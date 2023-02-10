import time
from typing import Optional

from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os
from os.path import isfile, join
import datetime
from typing import List
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils import find_sssb_element, nzip, nmap, find_2d, lists_equal

target = "https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/?actionId=&omraden=Lappis&oboTyper=BOAS1&hyraMax="
directory = "{}/sssbscraper".format(os.getenv('HOME'))
time_format = '%Y-%m-%d_%H-%M-%S'


def get_website_content(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')


def extract_data(website):
    id = find_sssb_element(website, 'h4', 'ObjektAdress', lambda e: e.find('a'))
    headlines = find_sssb_element(website, 'h3', 'ObjektTyp', lambda e: e.find('a'))

    raw_queue_days = find_sssb_element(website, 'dd', 'ObjektAntalIntresse')
    split = nzip(nmap(lambda e: e.split(' '), raw_queue_days))

    queue_days = split[0]
    no_applicants = nmap(lambda s: s[1:2], split[1])
    moving_in_date = find_sssb_element(website, 'dd', 'ObjektInflytt')
    size = find_sssb_element(website, 'dd', 'ObjektYta')
    rent = find_sssb_element(website, 'dd', 'ObjektHyra')
    floor = nmap(lambda s: s.strip(), find_sssb_element(website, 'dd', 'ObjektVaning'))

    t = [id, headlines, queue_days, no_applicants, moving_in_date, floor, size, rent]
    titles = ["Id", "Title", "Queue Days", "No. Applicants", "Moving in Date", "Flor", "Size", "Rent"]

    z = nzip(t)
    z.insert(0, titles)
    return z


def save_to_csv(data):
    file_name = "{directory}/{time}.csv".format(directory=directory, time=datetime.datetime.now().strftime(time_format))
    f = open(file_name, 'w')

    writer = csv.writer(f)

    for row in data:
        writer.writerow(row)

    f.close()


def find_most_recent_file_path() -> Optional[str]:
    files = [f for f in os.listdir(directory) if isfile(join(directory, f)) and f != ".DS_Store"]
    if len(files) == 0:
        return None
    sorted_files = sorted(files, key=lambda e: datetime.datetime.strptime(e.removesuffix('.csv'), time_format),
                          reverse=True)
    return "{directory}/{f}".format(directory=directory, f=sorted_files[0])


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
    prev_path = find_most_recent_file_path()
    content = get_website_content(target)
    data = extract_data(content)

    if prev_path is not None:
        previous = read_csv(prev_path)
        if any_diff(previous, data):
            print("{}: Found difference. Saving".format(datetime.datetime.now()))
            save_to_csv(data)
        else:
            print("Didn't find any difference. Not saving file")
    else:
        save_to_csv(data)

    print(data)


def loop():
    while True:
        print("{}: Scheduled execution".format(datetime.datetime.now()))
        run()
        time.sleep(60 * 5)


if __name__ == '__main__':
    loop()
