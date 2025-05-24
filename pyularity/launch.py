# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join, exists
from os import name
import datetime as dt
import subprocess
import socket
import threading

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "launch.yaml")


class Launch(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("Launch").override(cfg)
        self.concurrent_limit = self.config.dikt.get("concurrent_limit", 5)
        self.host = self.config.dikt.get("host", "127.0.0.1")
        self.is_installed = False
        self.port = self.config.dikt.get("port", 65432)
        self.processes = {}
        self.python_executable = None
        self.running = False
        self.venv_path = None

    def check_installed(self):
        """"""
        return self

    def check_process(self, pid):
        """
        Checks if a process is still running.

        :param pid: Process ID to check.
        :return: Boolean indicating whether the process is running.
        """
        if pid in self.processes:
            process = self.processes[pid]
            status = process.poll()
            if status is None:
                logma.info(f"Process {pid} is running.")
                return True
            else:
                logma.info(f"Process {pid} has stopped with exit code {status}.")
                del self.processes[pid]
                return False
        else:
            logma.info(f"Process with PID {pid} not found.")
            return False

    def check_update(self):
        """"""

    def close(self):
        """"""
        self.stop_all_processes()
        return self

    def initialize_communications_server(self):
        """"""
        self.comserv = threading.Trhead(target=self._start_server, daemon=True)
        self.comserv.start()
        self.running = True
        return self

    def launch_app(self):
        """"""
        cnt = 0
        while not self.check_installed():
            if cnt > 3:
                self.close()
                break
            while True:
                self.start_process("install")
                if not self.check_process(self.start_process("Install")):
                    break
            cnt += 1
        else:
            self.launch_instance()
        return self

    def launch_instance(self, instance_id=None, *args, **kwargs):
        """"""
        if instance_id is None:
            instance_id = ""
        if len(self.processes) > self.concurrent_limit:
            message = f"This Program is limited to {self.concurrent_limit} concurrent instances."
            message += f"Please wait for a free instance to launch."
            gui.show(message)
            return None

        self.start_process("run", instance_id)
        return self

    def run_update(self):
        """"""
        # Check for update via api.nchantdoffice.com
        # if update is available download the newest manifest
        # verify manifest against blockchain based hash?
        # run pip/uv update installed modules
        # run pip/uv install any new modules
        # restart all running processes
        return self

    def set_virtual_environment(self):
        """"""
        if not exists(self.venv_path):
            raise Exception("Python Not Properly Installed for Pyularity based Application")
        if name == "linux":
            self.python_executable = join(self.venv_path, "bin", "python")
        elif name == "posix":
            self.python_executable = join(self.venv_path, "bin", "python")
        elif name == "nt":
            self.python_executable = join(self.venv_path, "Scripts", "python.exe")
        else:
            raise Exception(f"Unknown OS Type: {name}")
        return self

    def start_process(self, script_path, *args):
        """
        Starts a Python script as a separate process.

        :param script_path: Path to the Python script to run.
        :param args: Additional arguments for the script.
        :return: Process ID.
        """
        cmd = [self.python_executable, script_path, *args]
        try:
            # Launch process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.processes[process.pid] = process
            logma.info(f"Started process with PID: {process.pid}")
            return process.pid
        except Exception as e:
            logma.info(f"Error starting process: {e}")
            return None

    def stop_process(self, pid):
        """
        Stops a process by sending a SIGTERM signal.

        :param pid: Process ID to stop.
        """
        if pid in self.processes:
            process = self.processes[pid]
            process.terminate()  # Send SIGTERM
            process.wait()  # Wait for the process to terminate
            logma.info(f"Terminated process with PID: {pid}")
            del self.processes[pid]
        else:
            logma.info(f"Process with PID {pid} not found.")

    def stop_all_processes(self):
        """
        Stops all managed processes.
        """
        logma.info("Stopping all processes...")
        for pid in list(self.processes.keys()):
            self.stop_process(pid)

    def stop_server(self):
        """Shuts down the callback server and all child processes."""
        self.running = False
        if hasattr(self, "server_socket"):
            self.server_socket.close()
        logma.info("Callback server and all processes have been stopped.")

    def _start_callback_server(self):
        """Starts the callback server that listens for messages from child processes."""
        logma.info(f"Starting callback server on {self.host}:{self.port}")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        while self.running:
            client_socket, address = self.server_socket.accept()
            logma.info(f"Connected to child process at {address}")
            threading.Thread(target=self._handle_client, args=(client_socket,), daemon=True).start()

    def _handle_client(self, client_socket):
        """Handles incoming messages from a child process."""
        with client_socket:
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    # Decode and logma.info the callback message
                    message = data.decode("utf-8").strip()
                    logma.info(f"[Callback Received]: {message}")
                    if "new_instance:" in message:
                        instance_id = message.split(":")[1]
                        self.launch_instance(instance_id)
                    # looking for calls to launch a new instance
                except Exception as e:
                    logma.info(f"Error receiving data from child process: {e}")
                    break


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
