import csv
import datetime
import glob
import itertools
import os

from config import DATA_DIR
from file_utils import move_files_to_folder


def dicts_to_csv(dict_list, fname, header=False):
    keys = dict_list[0].keys()
    with open(fname, "a", newline="") as f:
        dict_writer = csv.DictWriter(f, keys)
        if header:
            dict_writer.writeheader()
        dict_writer.writerows(dict_list)


def records_to_csv(records, fname):
    if not os.path.exists(fname):
        dicts_to_csv(records, fname, header=True)
    dicts_to_csv(records, fname)


def group_by_date(records):
    dates = []
    date_func = lambda x: x["Datetime"].date()
    for key, group in itertools.groupby(records, date_func):
        dates.append([g for g in group])
    return dates


def save_as_daily_files(records):
    dates = group_by_date(records)
    for d in dates:
        fname = f'{d[0].get("Datetime").strftime("%Y%m%d")}.csv'
        fpath = os.path.join(DATA_DIR, fname)
        records_to_csv(d, fpath)


def get_last_record():
    local_files = sorted(glob.glob(f"{DATA_DIR}/*.csv"))
    if len(local_files) > 0:
        with open(local_files[-1], "r") as f:
            last_line = f.readlines()[-1]
            last_record = last_line.split(",")[0]
            return datetime.datetime.strptime(last_record, "%Y-%m-%d %H:%M:%S")
    return datetime.datetime(2022, 9, 14, 23, 55)

def archive_past_days(local_files, dest_folder):
    if len(local_files) > 1:
        move_files_to_folder(local_files[:-1], dest_folder)