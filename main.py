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


def get_website(url):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(target)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    id = find(soup, 'h4', 'ObjektAdress', lambda e: e.find('a'))
    headlines = find(soup, 'h3', 'ObjektTyp', lambda e: e.find('a'))

    raw_queue_days = find(soup, 'dd', 'ObjektAntalIntresse')
    split = nzip(nmap(lambda e: e.split(' '), raw_queue_days))

    queue_days = split[0]
    no_applicants = nmap(lambda s: s[1:2], split[1])
    moving_in_date = find(soup, 'dd', 'ObjektInflytt')
    size = find(soup, 'dd', 'ObjektYta')
    rent = find(soup, 'dd', 'ObjektHyra')
    floor = nmap(lambda s: s.strip(), find(soup, 'dd', 'ObjektVaning'))

    t = [id, headlines, queue_days, no_applicants, moving_in_date, floor, size, rent]
    titles = ["Id", "Title", "Queue Days", "No. Applicants", "Moving in Date", "Flor", "Size", "Rent"]

    z = nzip(t)
    z.insert(0, titles)
    print(z)

    f = open("/Users/yannickknoll/Desktop/data.csv", 'w')

    writer = csv.writer(f)

    for row in z:
        writer.writerow(row)

    f.close()


if __name__ == '__main__':
    get_website('PyCharm')
