from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import os

from utils import find, nzip, nmap

target = "https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/?actionId=&omraden=Lappis&oboTyper=BOAS1&hyraMax="
path = "{}/Desktop/data.csv".format(os.getenv('HOME'))


def get_website_content(url):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(target)
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')


def extract_data(website):
    id = find(website, 'h4', 'ObjektAdress', lambda e: e.find('a'))
    headlines = find(website, 'h3', 'ObjektTyp', lambda e: e.find('a'))

    raw_queue_days = find(website, 'dd', 'ObjektAntalIntresse')
    split = nzip(nmap(lambda e: e.split(' '), raw_queue_days))

    queue_days = split[0]
    no_applicants = nmap(lambda s: s[1:2], split[1])
    moving_in_date = find(website, 'dd', 'ObjektInflytt')
    size = find(website, 'dd', 'ObjektYta')
    rent = find(website, 'dd', 'ObjektHyra')
    floor = nmap(lambda s: s.strip(), find(website, 'dd', 'ObjektVaning'))

    t = [id, headlines, queue_days, no_applicants, moving_in_date, floor, size, rent]
    titles = ["Id", "Title", "Queue Days", "No. Applicants", "Moving in Date", "Flor", "Size", "Rent"]

    z = nzip(t)
    z.insert(0, titles)
    return z


def save_to_csv(data):
    f = open(path, 'w')

    writer = csv.writer(f)

    for row in data:
        writer.writerow(row)

    f.close()


def run():
    content = get_website_content(target)
    data = extract_data(content)
    print(data)
    save_to_csv(data)


if __name__ == '__main__':
    run()
