from typing import Optional

from colorama import Fore
from selenium.common import TimeoutException

from defs import Table
from params import webdriver_timeout_secs
from utils import nmap, nzip, output
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver


def get_website_content(url) -> BeautifulSoup:
    options = Options()
    # Set headless mode to True so the browser runs in the background
    options.headless = True
    driver = webdriver.Chrome(options=options)

    # Fetch the site repeatedly until it is loaded
    html = None
    while html is None:
        html = fetch_site(driver, url)

    # Return dynamically generated html
    return BeautifulSoup(html, 'html.parser')


def fetch_site(driver, url) -> Optional[str]:
    try:
        output(Fore.LIGHTWHITE_EX + "Fetching site: {url}".format(url=url))
        driver.get(url)
        WebDriverWait(driver, webdriver_timeout_secs).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ObjektAntalIntresse')))
    except TimeoutException:
        output(Fore.RED + "Timed out waiting for page to load")
        return None
    return driver.page_source


def extract_sssb_data(website) -> Table:
    id = find_sssb_element(website, 'h4', 'ObjektAdress', lambda e: e.find('a'))
    headlines = find_sssb_element(website, 'h3', 'ObjektTyp', lambda e: e.find('a'))

    raw_queue_days = find_sssb_element(website, 'dd', 'ObjektAntalIntresse')
    split = nzip(nmap(lambda e: e.split(' '), raw_queue_days))

    queue_days = nmap(lambda e: int(e), split[0])
    no_applicants = nmap(lambda s: int(s.lstrip("(").rstrip("st)")), split[1])
    moving_in_date = find_sssb_element(website, 'dd', 'ObjektInflytt')

    def conv_num(s, suff):
        s = s.rstrip(suff).replace(u'\xa0', '')
        return int(s)

    rent = nmap(lambda e: conv_num(e, " kr"), find_sssb_element(website, 'dd', 'ObjektHyra'))

    size = nmap(lambda e: conv_num(e, ' m²'), find_sssb_element(website, 'dd', 'ObjektYta'))

    def conv_floor(s):
        s = s.strip()
        if s.isdigit():
            s = int(s)
        else:
            s = 0
        return s

    floor = nmap(conv_floor, find_sssb_element(website, 'dd', 'ObjektVaning'))

    columns = [id, headlines, queue_days, no_applicants, moving_in_date, floor, size, rent]
    titles = ["Id", "Title", "Queue Days", "No. Applicants", "Moving in Date", "Floor", "Size (m²)", "Rent (SEK)"]

    # Transpose from an array of columns to an array of rows to make it csv writeable
    rows = nzip(columns)
    rows.insert(0, titles)
    return rows


def find_sssb_element(soup, tag, clazz, func=None):
    res = soup.find_all(tag, attrs={'class': clazz})
    if func is not None:
        res = nmap(func, res)
    return nmap(lambda e: e.text, res)
