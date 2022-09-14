from ftplib import FTP
import logging
import pysftp

logger = logging.getLogger(__name__)


def upload_to_ftp(local_files, ftp_ip, ftp_user, ftp_password, ftp_dir):
    logger.debug("Uploading to FTP server...")
    with FTP(ftp_ip, ftp_user, ftp_password) as ftp:
        ftp.cwd(ftp_dir)
        for local_file in local_files:
            with open(local_file, "rb") as f:
                ftp.storbinary(f"STOR {local_file}", f)
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
