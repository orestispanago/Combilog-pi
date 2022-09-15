import os
import logging
import json
from types import SimpleNamespace

logger = logging.getLogger(__name__)


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


def json_file_to_object(fname):
    with open(fname) as f:
        python_object = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    return python_object
