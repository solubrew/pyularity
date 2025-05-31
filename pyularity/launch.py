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
import time
import subprocess
import socket
import threading

# ======================================3rd Party Library Modules=====================================================||
import zmq

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from pycurity.pyhash import text_hashing_function

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
        self.new_modules = []
        self.manifest = ""
        self.port = self.config.dikt.get("port", 65432)
        self.processes = {}
        self.python_executable = None
        self.scripts = None
        self.socket = None
        self.running = False
        self.venv_path = None

    def check_installed(self):
        """"""
        # Check for update via api.nchantdoffice.com
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
        return self

    def check_update(self):
        """"""
        return self

    def close(self):
        """"""
        self.stop_all_processes()
        return self

    def close_instance(self, instance_id):
        """"""
        self.stop_process(instance_id)
        if len(self.processes) == 0:
            self.stop_server()
        return self

    def compare_manifest(self, manifest):
        """"""
        self.new_modules = []
        for module in manifest:
            if module not in self.manifest:
                self.new_modules.append(module)
        return True

    def connect(self, server="tcp://127.0.0.1", port="5555"):
        """"""
        context = zmq.Context()  # Create a ZeroMQ context
        self.socket = context.socket(zmq.REP)  # Create a REP (Reply) socket
        self.socket.bind(f"{server}:{port}")  # Bind to a TCP address
        return self

    def get_hash(self, application_NCD):
        """"""
        _hash = ""  # connect to some blockchain service
        return _hash

    def get_manifest(self):
        """"""
        manifest = ""
        self.compare_manifest(manifest)
        if manifest != self.manifest:
            self.manifest = manifest
        return self

    def initialize_communications_server(self):
        """"""
        self.comserv = threading.Thread(target=self._start_server, daemon=True)
        self.comserv.start()
        self.running = True
        return self

    def launch_app(self):
        """"""
        cnt = 0
        if self.check_update():
            self.run_update()
        self.initialize_communications_server()
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
            message += f"Please close an instance to launch another."
            gui.show(message)
            return None
        self.start_process("run", instance_id)
        return self

    def restart_processes(self):
        """"""
        return self

    def run_update(self):
        """"""
        if self.check_update():
            self._download()
            self._install_modules()
            self._update_modules()
            self.restart_processes()
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
        return self

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
        return self

    def stop_all_processes(self):
        """
        Stops all managed processes.
        """
        logma.info("Stopping all processes...")
        for pid in list(self.processes.keys()):
            self.stop_process(pid)
        return self

    def stop_server(self):
        """Shuts down the callback server and all child processes."""
        self.running = False
        if hasattr(self, "server_socket"):
            self.server_socket.close()
        logma.info("Callback server and all processes have been stopped.")
        return self

    def _copy_to_install(self):
        """"""
        return self

    def _download(self):
        """"""
        self.manifest = self.get_manifest()
        self._copy_to_install()
        self._hash = text_hashing_function(self.manifest)
        return self

    def _install_modules(self):
        """"""
        for module in self.manifest:
            self.pip_install(module)
        return self

    def _start_server(self, *args, **kwargs):
        """"""
        self.connect()
        while True:
            # Wait for the next request from the client
            message = self.socket.recv_string()  # Receive UTF-8 string
            if message.split(":")[0] == "NEWINSTANCE":
                self.launch_instance(message.split(":")[1])
                self.socket.send_string("TRUE")  # Send UTF-8 string
            elif message.split(":")[0] == "CLOSEINSTANCE":
                self.close_instance(message.split(":")[1])
                self.socket.send_string("TRUE")
            elif message.split(":")[0] == "EXIT":
                self.close_instance(message.split(":")[1])
                break
            time.sleep(10)
        return self

    def _update_modules(self):
        """"""
        for module in self.manifest:
            self.pip_install(module)
        return self

    def _verify(self):
        """"""
        _hash = self.get_hash(self.application_NCD)
        if _hash != self._hash:
            return False
        return True


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
