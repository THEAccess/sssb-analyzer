import datetime
import time

from analyze import iterate_changes
from disk import get_current_working_dir, find_most_recent_file_path, read_csv, save_to_csv, read_dir
from params import base_url, run_interval_minutes_default, base_directory, analyze_file_name
from scraper import get_website_content, extract_sssb_data
from utils import output, any_diff


def run():
    working_dir = get_current_working_dir()
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


def scraper_loop():
    while True:
        output("Running scheduled execution")
        run()
        time.sleep(60 * run_interval_minutes_default)




if __name__ == '__main__':
    scraper_loop()
