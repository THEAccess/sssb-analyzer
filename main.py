# This is a sample Python script.
import time

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

target = "https://sssb.se/soka-bostad/sok-ledigt/lediga-bostader/?actionId=&omraden=Lappis&oboTyper=BOAS1&hyraMax="


def get_website(name):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(target)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    headlines = [h3.find('a').text for h3 in  soup.find_all('h3', attrs={'class': 'ObjektTyp'})]
    queueDays = soup.find_all('dd', attrs={ 'class': 'ObjektAntalInteresse'})
    movingInDate = soup.find_all('dd', attrs={ 'class': 'ObjektInflytt'})
    size = soup.find_all('dd', attrs={ 'class': 'ObjektYta'})
    hyra = soup.find_all('dd', attrs={ 'class': 'ObjektHyra'})
    floor = soup.find_all('dd', attrs={ 'class': 'Våning'})
    print(queueDays)  # Press ⌘F8 to toggle the breakpoint.
    print(movingInDate)  # Press ⌘F8 to toggle the breakpoint.
    print(size)  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_website('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
