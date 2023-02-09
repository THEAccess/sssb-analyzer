# This is a sample Python script.
import time

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
import requests

target = "https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/?actionId=&omraden=Lappis&oboTyper=BOAS1&hyraMax="


def nmap(func, array):
    return list(map(func, array))


def map_2d(func, array):
    return list(nmap(lambda nested_array: nmap(func, nested_array), array))


def find(soup, tag, clazz, func=None):
    res = soup.find_all(tag, attrs={'class': clazz})
    if func is not None:
        res = nmap(func, res)
    return nmap(lambda e: e.text, res)


def nzip(arr):
    return list(zip(*arr))


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
    f = open("/Users/yannickknoll/Desktop/data.csv", 'w')

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
