import logging
import logging.config
import os
import traceback
import glob
from config.config import DATA_DIR
from config.config import ftp_ip, ftp_user, ftp_password, ftp_dir
from uploader import upload_to_ftp
from datalogger import get_data_since_last_readout
from record_functions import save_as_daily_files

os.chdir(os.path.dirname(os.path.abspath(__file__)))


logging.config.fileConfig("config/logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def main():
    records = get_data_since_last_readout()
    save_as_daily_files(records)

    local_files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))
    upload_to_ftp(local_files, ftp_ip, ftp_user, ftp_password, ftp_dir)
    # archive_past_days(local_files, "archive")

    logger.debug(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
