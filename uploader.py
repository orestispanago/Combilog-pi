import logging
from ftplib import FTP
import os
import pysftp

logger = logging.getLogger(__name__)


def upload_to_ftp(local_files, ftp_config):
    base_names = [os.path.basename(x) for x in local_files]
    logger.debug("Uploading to FTP server...")
    with FTP(ftp_config.ip, ftp_config.user, ftp_config.passwd) as ftp:
        ftp.cwd(ftp_config.folder)
        for local_file, remote_file in zip(local_files, base_names):
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {remote_file}", f)
    logger.info(f"Uploaded {len(local_files)} files.")


def upload_to_sftp(
    local_files,
    sftp_host,
    sftp_user,
    sftp_password,
    known_hosts_file,
    sftp_dir,
    sftp_subdir,
):
    cnopts = pysftp.CnOpts(knownhosts=known_hosts_file)
    logger.debug("Uploading to SFTP server...")
    with pysftp.Connection(
        sftp_host, username=sftp_user, password=sftp_password, cnopts=cnopts
    ) as sftp:
        sftp.cwd(sftp_dir)
        if sftp_subdir not in sftp.listdir():
            sftp.mkdir(sftp_subdir)
        sftp.chdir(sftp_subdir)
        for local_file in local_files:
            sftp.put(local_file)
    logger.info(f"Uploaded {len(local_files)} files.")
