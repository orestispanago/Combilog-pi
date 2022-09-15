import logging
import logging.config
import os
import traceback

from config import DATA_DIR, SRC_DIR

# from uploader import upload_to_ftp, archive_past_days
from datalogger import get_data_since_last_readout
from record_functions import save_as_daily_files

os.chdir(SRC_DIR)


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def main():
    records = get_data_since_last_readout()
    save_as_daily_files(records)

    # local_files = sorted(glob.glob("*.csv"))
    # upload_to_ftp(local_files, FTP_IP, FTP_USER, FTP_PASS, FTP_DIR)
    # archive_past_days(local_files, "archive")

    logger.debug(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
