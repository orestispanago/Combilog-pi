import os
import itertools
import csv


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
        output_file = f'{d[0].get("Datetime").strftime("%Y%m%d")}.csv'
        records_to_csv(d, output_file)
