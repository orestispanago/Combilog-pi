import glob
import logging
import logging.config
import os
import traceback

from datalogger import DATA_DIR, Datalogger
from uploaders import ftp_upload_files_list, sftp_upload_files_list
from utils import archive_past_days

os.chdir(os.path.dirname(os.path.abspath(__file__)))


logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("paramiko").setLevel(logging.WARNING)


def main():
    datalogger = Datalogger()
    datalogger.set_time_utc()
    datalogger.get_data_since_last_readout()
    datalogger.save_as_daily_files()
    local_files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))
    ftp_upload_files_list(local_files)
    sftp_upload_files_list(local_files)
    archive_past_days(local_files)
    logger.debug(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
