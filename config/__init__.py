import json
from file_utils import mkdir_if_not_exists
from types import SimpleNamespace

# paths are relative to main.py
DATA_DIR = "data"
LOG_DIR = "logs"

mkdir_if_not_exists("logs")
mkdir_if_not_exists("data")


sftp_host = ""
sftp_user = ""
sftp_password = ""
sftp_dir = ""
sftp_subdir = ""
known_hosts_file = ""

# DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

with open("config/ftp.json") as f:
    FTP_CONFIG = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
