import logging
from ftplib import FTP
import os
import pysftp

logger = logging.getLogger(__name__)


def upload_to_ftp(local_files, ip, user, passwd, folder):
    base_names = [os.path.basename(x) for x in local_files]
    logger.debug("Uploading to FTP server...")
    with FTP(ip, user, passwd) as ftp:
        ftp.cwd(folder)
        for local_file, remote_file in zip(local_files, base_names):
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {remote_file}", f)
    logger.info(f"Uploaded {len(local_files)} files to FTP.")


def upload_to_sftp(local_files, host, user, passwd, known_hosts, folder, subfolder):
    cnopts = pysftp.CnOpts(knownhosts=known_hosts)
    logger.debug("Uploading to SFTP server...")
    with pysftp.Connection(host, username=user, password=passwd, cnopts=cnopts) as sftp:
        sftp.cwd(folder)
        if subfolder not in sftp.listdir():
            sftp.mkdir(subfolder)
        sftp.chdir(subfolder)
        for local_file in local_files:
            sftp.put(local_file)
    logger.info(f"Uploaded {len(local_files)} files to SFTP.")
