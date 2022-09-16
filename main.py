import logging
import logging.config
import os
import traceback
import glob
from uploader import upload_to_ftp, upload_to_sftp
from datalogger import get_data_since_last_readout
from record_functions import archive_past_days, save_as_daily_files


ftp_ip = ""
ftp_user = ""
ftp_password = ""
ftp_dir = "datalogger/test"


sftp_host = ""
sftp_user = ""
sftp_password = ""
known_hosts_file = "known_hosts"
sftp_dir = ""
sftp_subdir = ""


logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("paramiko").setLevel(logging.CRITICAL + 1)


def main():
    records = get_data_since_last_readout("data")
    save_as_daily_files(records, "data")

    local_files = sorted(glob.glob(f"data/*.csv"))
    upload_to_ftp(local_files, ftp_ip, ftp_user, ftp_password, ftp_dir)
    upload_to_sftp(
        local_files,
        sftp_host,
        sftp_user,
        sftp_password,
        known_hosts_file,
        sftp_dir,
        sftp_subdir,
    )
    archive_past_days(local_files, f"data/archive")
    logger.debug(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())

