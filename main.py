import datetime
import time

from disk import get_current_working_dir, find_most_recent_file_path, read_csv, save_to_csv
from params import base_url, run_interval_minutes_default
from scraper import get_website_content, extract_sssb_data
from utils import output, any_diff, get_arg


def run(directory: str):
    working_dir = get_current_working_dir(directory)
    # Get the path of the csv file for the most recent data fetched before this run (if it exists)
    prev_file_path = find_most_recent_file_path(working_dir)
    html_content = get_website_content(base_url)
    data = extract_sssb_data(html_content)

    output(data)

    if prev_file_path is not None:
        previous = read_csv(prev_file_path)
        if any_diff(previous, data):
            output("{}: Found difference. Saving".format(datetime.datetime.now()))
            save_to_csv(data, working_dir)
        else:
            output("Didn't find any difference. Not saving file")
    else:
        save_to_csv(data, working_dir)


def loop(directory: str):
    output("Saving results to: {}".format(directory))
    output("This programme will run indefinitely until terminated.")
    while True:
        output("Running scheduled execution")
        run(directory)
        time.sleep(60 * run_interval_minutes_default)


if __name__ == '__main__':
    base_dir = get_arg("base_dir", 0)
    loop(base_dir)
