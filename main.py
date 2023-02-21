import time
from disk import get_current_working_dir, find_most_recent_file_path, read_csv, save_to_csv
from params import base_url, run_interval_minutes_default, closing_time_proximity_threshold
from scraper import get_website_content, extract_sssb_data
from timeutils import is_next_SSSB_closing_time_near
from utils import output, any_diff, get_arg, pprint_conv, url_fix_show_all
from colorama import Fore
import optparse


def run(directory: str, url: str):
    working_dir = get_current_working_dir(directory)
    # Get the path of the csv file for the most recent data fetched before this run (if it exists)
    prev_file_path = find_most_recent_file_path(working_dir)
    html_content = get_website_content(url)
    data = extract_sssb_data(html_content)

    print(pprint_conv(data))

    if prev_file_path is not None:
        previous = read_csv(prev_file_path)[0]
        if any_diff(previous, data):
            output(Fore.GREEN + "Found difference. Saving .csv file")
            save_to_csv(data, working_dir)
        else:
            output("Didn't find any difference. Not saving file")
    else:
        save_to_csv(data, working_dir)


def loop(directory: str, url: str):
    output("Saving results to: {}".format(directory))
    output(Fore.MAGENTA + "This programme will run indefinitely until terminated.")
    while True:
        output(Fore.YELLOW + "Running scheduled execution")
        run(directory, url)
        next_delay = determine_delay()
        output("Next execution in {} seconds".format(next_delay))
        time.sleep(next_delay)


def determine_delay():
    delay = run_interval_minutes_default * 60
    if is_next_SSSB_closing_time_near(10):
        delay = 0
        output(Fore.CYAN + "Closing time close. Running more often")
    elif is_next_SSSB_closing_time_near(60):
        delay = 30
        output(Fore.CYAN + "Closing time close. Running more often")
    return delay


if __name__ == '__main__':
    base_dir = get_arg("base_dir", 0)
    p = optparse.OptionParser()
    p.add_option('--url', '-u', default=base_url)
    options, _ = p.parse_args()
    loop(base_dir, url_fix_show_all(options.url))
