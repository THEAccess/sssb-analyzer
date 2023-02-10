from typing import Optional
import csv
from typing import List
import datetime
from date import closest_monday_16_or_thursday_10
from os.path import isfile, join
import os
from constants import directory, disk_time_format


def save_to_csv(data, path):
    f = open("{p}/{f}.csv".format(p=path, f=datetime.datetime.now().strftime(disk_time_format)), 'w')

    writer = csv.writer(f)

    for row in data:
        writer.writerow(row)

    f.close()


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
    path = "{directory}/{d}".format(directory=directory,
                                    d=closest_monday_16_or_thursday_10().strftime(disk_time_format))

    dir = path.rsplit('/', 1)[0]

    if not os.path.isdir(dir):
        os.mkdir(dir)

    return path


def read_csv(path) -> List[List[str]]:
    # opening the CSV file
    res = []
    with open(path, mode='r') as file:
        # reading the CSV file
        f = csv.reader(file)

        # displaying the contents of the CSV file
        for lines in f:
            res.append(lines)
    return res
