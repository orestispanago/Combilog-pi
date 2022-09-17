import datetime
import logging
import os
import glob
import itertools
import csv
import combilog


logger = logging.getLogger(__name__)

DATA_DIR = "data"


class Datalogger:
    def __init__(self, port="/dev/ttyACM0"):
        self.device = combilog.Combilog(logger_addr=1, port=port, baudrate=38400)
        self.pointers = {1: "E", 2: "e"}
        self.records = []
        self.last_readout = ""
        self.channel_names = ["Datetime"]

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
            print(f"Read {i} of {num_records} records", sep="", end="\r", flush=True)
        logger.info(f"Retrieved {len(self.records)} records.")
        return self.records

    def read_record(self, pointer: int):
        pointer_char = self.pointers[pointer]
        with self.device.ser as ser:
            telegram = f"${self.device.logger_addr}{pointer_char}\r".encode("latin-1")
            ser.write(telegram)
            resp = ser.read_until(b"\r")
        if len(resp) > 3:
            resp_decoded = resp.decode("latin-1")[1:].split(";")
            # the first char is the address and therefore not needed
            date = datetime.datetime.strptime(resp_decoded[0][1:], "%y%m%d%H%M%S")
            # remove carriage return at the end
            # and convert from IEE Std 754 Short Real Format
            channel_values = [date]
            for i in resp_decoded[1:-1]:
                channel_values.append(combilog._hexIEE_to_dec(i))
            record = {
                key: value for key, value in zip(self.channel_names, channel_values)
            }
            return record
        else:
            return {}

    def get_last_readout(self):
        local_files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))
        if len(local_files) > 0:
            with open(local_files[-1], "r") as f:
                last_line = f.readlines()[-1]
                last_readout_str = last_line.split(",")[0]
                last_readout = datetime.datetime.strptime(
                    last_readout_str, "%Y-%m-%d %H:%M:%S"
                )
                return last_readout
        else:
            logger.debug("No .csv file found. Reading all datalogger memory...")
            return datetime.datetime(2022, 9, 14, 23, 55)

    def get_data_since_last_readout(self):
        self.device.pointer_to_date(
            1, self.get_last_readout() + datetime.timedelta(seconds=1)
        )
        self.readout(pointer=1)

    def group_records_by_date(self):
        dates = []
        date_func = lambda x: x["Datetime"].date()
        for key, group in itertools.groupby(self.records, date_func):
            dates.append([g for g in group])
        return dates

    def save_as_daily_files(self):
        dates = self.group_records_by_date()
        for d in dates:
            fname = f'{d[0].get("Datetime").strftime("%Y%m%d")}.csv'
            fpath = os.path.join(DATA_DIR, fname)
            if not os.path.exists(fpath):
                dicts_to_csv(d, fpath, header=True)
            dicts_to_csv(d, fpath)


def dicts_to_csv(dict_list, fname, header=False):
    keys = dict_list[0].keys()
    with open(fname, "a", newline="") as f:
        dict_writer = csv.DictWriter(f, keys)
        if header:
            dict_writer.writeheader()
        dict_writer.writerows(dict_list)
    logger.debug(f"Wrote {len(dict_list)} lines in {fname}")


def mkdir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def move_files_to_folder(src_files, dest_folder):
    mkdir_if_not_exists(dest_folder)
    src_basenames = [os.path.basename(f) for f in src_files]
    for src_file, src_basename in zip(src_files, src_basenames):
        dest_file = f"{dest_folder}/{src_basename}"
        os.rename(src_file, dest_file)
        logger.info(f"Renamed file {src_file} to {dest_file}")


def archive_past_days(local_files, dest_folder):
    if len(local_files) > 1:
        move_files_to_folder(local_files[:-1], dest_folder)
