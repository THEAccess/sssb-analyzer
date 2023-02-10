from typing import Optional
import csv
from typing import List
import datetime
from date import next_closest_SSSB_closing_time
from os.path import isfile, join
import os

from defs import Table
from params import base_directory, disk_time_format, analyze_file_name
from utils import output


def save_to_csv(data: Table, path, name = None):
    n = datetime.datetime.now().strftime(disk_time_format)
    if name is not None:
        n = name
    with open("{p}/{f}.csv".format(p=path, f=n), 'w') as f:
        writer = csv.writer(f)

        for row in data:
            writer.writerow(row)


def find_most_recent_file_path(path) -> Optional[str]:
    if not os.path.isdir(path):
        return None
    files = [f for f in os.listdir(path) if isfile(join(path, f)) and f != ".DS_Store"]
    if len(files) == 0:
        return None
    sorted_files = sorted(files, key=lambda e: datetime.datetime.strptime(e.removesuffix('.csv'), disk_time_format),
                          reverse=True)
    return "{path}/{f}".format(path=path, f=sorted_files[0])


def get_current_working_dir() -> str:
    path = "{directory}/{d}".format(directory=base_directory,
                                    d=next_closest_SSSB_closing_time().strftime(disk_time_format))

    dir = path.rsplit('/', 1)[0]

    if not os.path.isdir(dir):
        os.mkdir(dir)

    return path


def read_csv(path) -> Table:
    # opening the CSV file
    res = []
    with open(path, mode='r') as file:
        # reading the CSV file
        f = csv.reader(file)

        # displaying the contents of the CSV file
        for lines in f:
            res.append(lines)
    res.pop(0)
    return res


def read_dir(directory) -> List[Table]:
    res = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if not filename.startswith(".") and not filename == analyze_file_name:
                p = os.path.join(root, filename)
                output("Reading {}".format(p))
                res.append(read_csv(p))
    return res
