import logging
import os
from ftplib import FTP, error_perm

import pysftp

logger = logging.getLogger(__name__)


SFTP_HOST = ""
SFTP_USER = ""
SFTP_PASSWORD = ""
SFTP_DIR = "/test"
SFTP_SUBDIR = "suntracker"
KNOWN_HOSTS_FILE = "known_hosts"


FTP_IP = ""
FTP_USER = ""
FTP_PASSWORD = ""
FTP_DIR = "/dataloggers/test"


def ftp_mkdir_and_enter(ftp_session, dir_name):
    if dir_name not in ftp_session.nlst():
        ftp_session.mkd(dir_name)
        logger.debug(f"Created FTP directory {dir_name}")
    ftp_session.cwd(dir_name)


def ftp_make_dirs(ftp_session, folder_path):
    for f in folder_path.split("/"):
        ftp_mkdir_and_enter(ftp_session, f)


def ftp_upload_file(ftp_session, local_path, remote_path):
    with open(local_path, "rb") as f:
        ftp_session.storbinary(f"STOR {remote_path}", f)
    logger.info(f"Uploaded {local_path} to {remote_path} at FTP")


def ftp_upload_files_list(local_files):
    with FTP(FTP_IP, FTP_USER, FTP_PASSWORD) as ftp:
        ftp.cwd(FTP_DIR)
        for local_file in local_files:
            base_name = os.path.basename(local_file)
            year = base_name[:4]
            remote_path = f"{year}/{base_name}"
            try:
                ftp_upload_file(ftp, local_file, remote_path)
            except error_perm as e:
                if "55" in str(e):
                    ftp_make_dirs(ftp, os.path.dirname(remote_path))
                    ftp.cwd(FTP_DIR)
                    ftp_upload_file(ftp, local_file, remote_path)


def sftp_upload_files_list(local_files):
    cnopts = pysftp.CnOpts(knownhosts=KNOWN_HOSTS_FILE)
    logger.debug("Uploading to SFTP server...")
    with pysftp.Connection(
        SFTP_HOST, username=SFTP_USER, password=SFTP_PASSWORD, cnopts=cnopts
    ) as sftp:
        sftp.cwd(SFTP_DIR)
        if SFTP_SUBDIR not in sftp.listdir():
            sftp.mkdir(SFTP_SUBDIR)
        sftp.chdir(SFTP_SUBDIR)
        for local_file in local_files:
            sftp.put(local_file)
            logger.debug(f"Uploaded {local_file} to SFTP")
    logger.info(f"Uploaded {len(local_files)} files to SFTP.")
