import csv
import datetime
import glob
import itertools
import logging
import os

import combilog

logger = logging.getLogger(__name__)

DATA_DIR = "data"


class Datalogger:
    def __init__(self, port="/dev/ttyACM0"):
        self.device = combilog.Combilog(
            logger_addr=1, port=port, baudrate=38400
        )
        self.pointers = {1: "E", 2: "e"}
        self.records = []
        self.last_readout = ""
        self.channel_names = ["Datetime_UTC"]

    def set_time_utc(self):
        logger.debug("Setting datalogger time to UTC")
        logger.debug(f"Current datalogger time: {self.device.read_datetime()}")
        self.device.set_datetime(datetime.datetime.utcnow())
        logger.debug(
            f"Datalogger time after update: {self.device.read_datetime()}"
        )

    def get_channel_names(self):
        num_channels = self.device.device_info().get("nr_channels")
        for chan in range(1, num_channels + 1):
            channel_name = self.device.get_channel_info(f"{chan:02}").get(
                "channel_notation"
            )
            self.channel_names.append(channel_name)
        return self.channel_names

    def readout(self, pointer: int):
        self.get_channel_names()
        # get number of logs
        num_records = self.device.get_nr_events()
        logger.debug(f"Found {num_records} records.")
        for i in range(num_records):
            record = self.read_record(pointer)
            self.records.append(record)
            print(
                f"Read {i} of {num_records} records",
                sep="",
                end="\r",
                flush=True,
            )
        logger.info(f"Retrieved {len(self.records)} records.")
        return self.records

    def read_record(self, pointer: int):
        pointer_char = self.pointers[pointer]
        with self.device.ser as ser:
            telegram = f"${self.device.logger_addr}{pointer_char}\r".encode(
                "latin-1"
            )
            ser.write(telegram)
            resp = ser.read_until(b"\r")
        if len(resp) > 3:
            resp_decoded = resp.decode("latin-1")[1:].split(";")
            # the first char is the address and therefore not needed
            date = datetime.datetime.strptime(
                resp_decoded[0][1:], "%y%m%d%H%M%S"
            )
            # remove carriage return at the end
            # and convert from IEE Std 754 Short Real Format
            channel_values = [date]
            for i in resp_decoded[1:-1]:
                channel_values.append(combilog._hexIEE_to_dec(i))
            record = {
                key: value
                for key, value in zip(self.channel_names, channel_values)
            }
            return record
        else:
            return {}

    def get_data_since_last_readout(self):
        self.device.pointer_to_date(
            1, get_last_readout() + datetime.timedelta(seconds=1)
        )
        self.readout(pointer=1)

    def group_records_by_date(self):
        dates = []
        date_func = lambda x: x["Datetime_UTC"].date()
        for key, group in itertools.groupby(self.records, date_func):
            dates.append([g for g in group])
        return dates

    def save_as_daily_files(self):
        dates = self.group_records_by_date()
        for d in dates:
            fname = f'{d[0].get("Datetime_UTC").strftime("%Y%m%d")}.csv'
            fpath = os.path.join(DATA_DIR, fname)
            if not os.path.exists(fpath):
                dicts_to_csv(d, fpath, header=True)
            else:
                dicts_to_csv(d, fpath)


def dicts_to_csv(dict_list, fname, header=False):
    keys = dict_list[0].keys()
    with open(fname, "a", newline="") as f:
        dict_writer = csv.DictWriter(f, keys)
        if header:
            dict_writer.writeheader()
        dict_writer.writerows(dict_list)
    logger.debug(f"Wrote {len(dict_list)} lines in {fname}")


def remove_last_line(fname):
    with open(fname, "r") as rf:
        lines = rf.readlines()
    with open(fname, "w") as wf:
        wf.writelines(lines[:-2])
    logger.warning(f"Removed last line from {fname}")


def get_last_readout_from_file(fname):
    with open(fname, "r") as f:
        last_line = f.readlines()[-1]
    last_record = last_line.split(",")[0]
    logger.debug(f"Last record: {last_record}")
    return datetime.datetime.strptime(last_record, "%Y-%m-%d %H:%M:%S")


def get_last_readout():
    local_files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))
    if len(local_files) > 0:
        last_file = local_files[-1]
        try:
            return get_last_readout_from_file(last_file)
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            logger.warning(f"removing last line from {last_file}")
            remove_last_line(last_file)
            return get_last_readout_from_file(last_file)
    logger.warning("No .csv file found, will read all datalogger memory...")
    return datetime.datetime(1990, 1, 1, 0, 0, 1)
