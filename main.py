import time

import datetime

from disk import get_current_working_dir, find_most_recent_file_path, read_csv, save_to_csv
from scraper import get_website_content, extract_sssb_data
from utils import find_2d, lists_equal, output
from constants import target, console_time_format


def any_diff(current, new) -> bool:
    return not find_diff(current, new)


def find_diff(current, new):
    res = list()
    current.pop(0)
    new.pop(0)
    for entry in current:
        opposite = find_2d(entry[0], new, 0)
        if opposite is not None and not lists_equal(new, opposite):
            res.append(opposite)
    return res


def run():
    current_dir = get_current_working_dir()
    prev_path = find_most_recent_file_path(current_dir)
    content = get_website_content(target)
    data = extract_sssb_data(content)

    if prev_path is not None:
        previous = read_csv(prev_path)
        if any_diff(previous, data):
            print("{}: Found difference. Saving".format(datetime.datetime.now()))
            save_to_csv(data, current_dir)
        else:
            print("Didn't find any difference. Not saving file")
    else:
        save_to_csv(data, current_dir)

    print(data)


def loop():
    while True:
        output("Running scheduled execution")
        run()
        time.sleep(60 * 5)


if __name__ == '__main__':
    loop()
