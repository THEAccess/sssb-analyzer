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


def get_website(name):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(target)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    headlines = nmap(lambda h3: h3.find('a'), soup.find_all('h3', attrs={'class': 'ObjektTyp'}))
    raw_queue_days = soup.find_all('dd', attrs={'class': 'ObjektAntalIntresse'})
    moving_in_date = soup.find_all('dd', attrs={'class': 'ObjektInflytt'})
    size = soup.find_all('dd', attrs={'class': 'ObjektYta'})
    rent = soup.find_all('dd', attrs={'class': 'ObjektHyra'})
    floor = soup.find_all('dd', attrs={'class': 'ObjektVaning'})

    t = [headlines, raw_queue_days, moving_in_date, size, rent, floor]
    titles = ["Title", "Queue Days", "No. Applicants", "Moving in Date", "Flor", "Size", "Rent"]
    r = map_2d(lambda e: e.text, t)

    z = list(zip(*r))
    z.insert(0, titles)
    print(list(r))
    print(z)


if __name__ == '__main__':
    get_website('PyCharm')
