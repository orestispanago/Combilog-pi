import os

from file_utils import mkdir_if_not_exists

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PARENT_DIR, "data")
LOG_DIR = os.path.join(PARENT_DIR, "logs")

mkdir_if_not_exists(LOG_DIR)
mkdir_if_not_exists(DATA_DIR)

ftp_ip = ""
ftp_user = ""
ftp_password = ""
ftp_dir = ""


sftp_host = ""
sftp_user = ""
sftp_password = ""
sftp_dir = ""
sftp_subdir = ""
known_hosts_file = ""

# DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
