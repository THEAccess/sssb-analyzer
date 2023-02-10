from utils import nmap, nzip
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def get_website_content(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.minimize_window()
    driver.get(url)
    time.sleep(4)
    html = driver.page_source
    return BeautifulSoup(html, 'html.parser')


def extract_sssb_data(website):
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


def find_sssb_element(soup, tag, clazz, func=None):
    res = soup.find_all(tag, attrs={'class': clazz})
    if func is not None:
        res = nmap(func, res)
    return nmap(lambda e: e.text, res)
