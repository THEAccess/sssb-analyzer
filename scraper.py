from defs import Table
from utils import nmap, nzip
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver


def get_website_content(url):
    options = Options()
    # Set headless mode to True so the browser runs in the background
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    # wait until element on page is located
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ObjektAntalIntresse')))
    html = driver.page_source
    # Return dynamically generated html
    return BeautifulSoup(html, 'html.parser')


def extract_sssb_data(website) -> Table:
    id = find_sssb_element(website, 'h4', 'ObjektAdress', lambda e: e.find('a'))
    headlines = find_sssb_element(website, 'h3', 'ObjektTyp', lambda e: e.find('a'))

    raw_queue_days = find_sssb_element(website, 'dd', 'ObjektAntalIntresse')
    split = nzip(nmap(lambda e: e.split(' '), raw_queue_days))

    queue_days = nmap(lambda e: int(e), split[0])
    no_applicants = nmap(lambda s: int(s[1:2]), split[1])
    moving_in_date = find_sssb_element(website, 'dd', 'ObjektInflytt')
    size = find_sssb_element(website, 'dd', 'ObjektYta')
    rent = find_sssb_element(website, 'dd', 'ObjektHyra')
    floor = nmap(lambda s: s.strip(), find_sssb_element(website, 'dd', 'ObjektVaning'))

    columns = [id, headlines, queue_days, no_applicants, moving_in_date, floor, size, rent]
    titles = ["Id", "Title", "Queue Days", "No. Applicants", "Moving in Date", "Flor", "Size", "Rent"]

    # Transpose from an array of columns to an array of rows to make it csv writeable
    rows = nzip(columns)
    rows.insert(0, titles)
    return rows


def find_sssb_element(soup, tag, clazz, func=None):
    res = soup.find_all(tag, attrs={'class': clazz})
    if func is not None:
        res = nmap(func, res)
    return nmap(lambda e: e.text, res)
