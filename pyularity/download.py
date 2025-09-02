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
from os.path import abspath, dirname, join
from sys import argv
import datetime as dt
import urllib

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def download_python(path, platform="linux", version="3.13"):
    """
    :return:
    """
    if platform == "linux":
        python_url = f"https://www.python.org/ftp/python/{version}/Python-{version}.tgz"
        python_archive = path / "Python.tgz"
    elif platform == "windows":
        python_url = f"https://www.python.org/ftp/python/{version}/python-{version}-embed-amd64.zip"
        python_archive = path / "python-embed.zip"
    elif platform == "macos":
        python_url = f"https://www.python.org/ftp/python/{version}/Python-{version}.tgz"
        python_archive = path / "Python.tgz"
    elif platform == "chromeos":
        python_url = f"https://www.python.org/ftp/python/{version}/python-{version}-embed-amd64.zip"
        python_archive = path / "python-embed.zip"
    else:
        raise ValueError(f"Unsupported platform: {platform}")
    urllib.request.urlretrieve(python_url, str(python_archive))


def run(args):
    """"""
    path = args[1]
    version = args[2] or "3.13"
    download_python(path, version)


if __name__ == "__main__":
    start = dt.datetime.now()
    logma.info("Start")
    run(argv)
    end = dt.datetime.now()
    logma.info(f"End Duration {end - start}")

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
