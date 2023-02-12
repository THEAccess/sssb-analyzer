from typing import Optional, Union
import csv
from typing import List
import datetime
from date import next_closest_SSSB_closing_time
from os.path import isfile, join
import os

from defs import Table
from params import disk_time_format, analyze_suffix
from utils import output


def save_to_csv(data: Table, path, name=None):
    n = datetime.datetime.now().strftime(disk_time_format)
    if name is not None:
        n = name
    with open("{p}/{f}.csv".format(p=path, f=n), 'w') as f:
        writer = csv.writer(f)

        for row in data:
            writer.writerow(row)


def all_csv_files(path) -> List[str]:
    if not os.path.isdir(path):
        return []
    return [f for f in os.listdir(path) if isfile(join(path, f)) and f.endswith(".csv")]


def find_most_recent_file_path(path) -> Optional[str]:
    files = all_csv_files(path)
    if len(files) == 0:
        return None
    sorted_files = sorted(files, key=lambda e: datetime.datetime.strptime(e.removesuffix('.csv'), disk_time_format),
                          reverse=True)
    return "{path}/{f}".format(path=path, f=sorted_files[0])


def get_current_working_dir(base_dir) -> str:
    path = "{directory}/{d}".format(directory=base_dir,
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
        for row in f:
            res.append(conv_row(row))
    res.pop(0)
    return res


def conv_row(row: List[str]) -> List[Union[str, int]]:
    res = []
    for e in row:
        try:
            res.append(int(e))
        except:
            res.append(e)
    return res


def read_dir(directory) -> List[Table]:
    res = []
    for item in os.listdir(directory):
        p = os.path.join(directory, item)
        if os.path.isfile(p) and not item.startswith(".") and not analyze_suffix in item:
            output("Reading {}".format(p))
            res.append(read_csv(p))
    return res
