import logging
import logging.config
import os
import traceback
import glob
from uploaders import upload_to_ftp, upload_to_sftp
from datalogger import Datalogger, archive_past_days, DATA_DIR


os.chdir(os.path.dirname(os.path.abspath(__file__)))


logger = logging.getLogger(__name__)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logging.getLogger("paramiko").setLevel(logging.CRITICAL + 1)


def main():
    datalogger = Datalogger()
    datalogger.get_data_since_last_readout()
    datalogger.save_as_daily_files()
    local_files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))
    upload_to_ftp(local_files)
    upload_to_sftp(local_files)
    archive_past_days(local_files, f"{DATA_DIR}/archive")
    logger.debug(f"{'-' * 15} SUCCESS {'-' * 15}")


if __name__ == "__main__":
    try:
        main()
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())

