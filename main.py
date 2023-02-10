import datetime
import time

from disk import get_current_working_dir, find_most_recent_file_path, read_csv, save_to_csv
from params import base_url
from scraper import get_website_content, extract_sssb_data
from utils import output, any_diff


def run():
    current_dir = get_current_working_dir()
    prev_path = find_most_recent_file_path(current_dir)
    content = get_website_content(base_url)
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
