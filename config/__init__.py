from file_utils import json_file_to_object, mkdir_if_not_exists

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

FTP_CONFIG = json_file_to_object("config/ftp.json")
