import overriden
import datetime
import combilog
import glob

# import logging


# logger = logging.getLogger(__name__)


combilog.Combilog.get_channel_list = overriden.get_channel_list
combilog.Combilog.read_logger = overriden.read_logger
combilog.Combilog.read_event = overriden.read_event


def get_last_record():
    local_files = sorted(glob.glob("*.csv"))
    if len(local_files) > 0:
        with open(local_files[-1], "r") as f:
            last_line = f.readlines()[-1]
            last_record = last_line.split(",")[0]
            return datetime.datetime.strptime(last_record, "%Y-%m-%d %H:%M:%S")
    return datetime.datetime(2022, 9, 13, 23, 55)


def get_data_since_last_readout():
    last_record = get_last_record()
    # logger.debug("Connecting to device...")

    device = combilog.Combilog(logger_addr=1, port="/dev/ttyACM0", baudrate=38400)
    device.get_channel_list()
    # logger.debug("Connection successfull. Retrieving data...")

    device.pointer_to_date(1, last_record + datetime.timedelta(seconds=1))
    records = device.read_logger(pointer=1)
    # logger.info(f"Retrieved {len(records)} records.")

    return records
