from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireOptions
from bs4 import BeautifulSoup
import time
import argparse
import threading
import json
import os
import re

GRAILED_BASE_URL = "https://www.grailed.com/categories/"

def init_of_driver(url):
    #options = ChromeOptions()
    options = FireOptions()
    options.add_argument('--disable-logging')
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = webdriver.Firefox(options)
    #driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver

def scroll_for_set_amout_of_sec(driver, secScroll, timeout=0.1):
    end_time = time.time() + secScroll
    while time.time() < end_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)

def bfsoup_parse_of_html_and_add_to_df(html_content):
    GRAILED_HOME_URL = "https://www.grailed.com"
    soup = BeautifulSoup(html_content, 'html.parser')
    feed_items = soup.find_all(class_='feed-item')
    iteration = 0
    for feed_item in feed_items:
        try:
            saved_links = {}
            iteration += 1
            saved_links['listing_link'] = GRAILED_HOME_URL + feed_item.find('a', class_='listing-item-link')['href']
            saved_links['img_link'] = re.sub(r'\?.*$', '', feed_item.find('img', class_='Image-module__crop___nWp1j')['src'])
            saved_links['similar_link'] = GRAILED_BASE_URL + feed_item.find('a', class_='SeeSimilarLink-module__link___tioRk')['href']
            saved_links['time_of_scrapping'] = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            save_to_json_file(saved_links, iteration)
        except TypeError:
            break

def save_to_json_file(saved_links, iteration):
    folder_path = 'json_dataset'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filename = f"{saved_links['time_of_scrapping']}_nr{iteration}.json"
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as json_file:
        json.dump(saved_links, json_file, indent=4)

def scrape_html(link, secScroll, categorie):
    url = link + categorie
    driver = init_of_driver(url)
    scroll_for_set_amout_of_sec(driver, secScroll)
    parent_element = driver.find_element(By.CLASS_NAME, "feed")
    html_content = parent_element.get_attribute('outerHTML')
    bfsoup_parse_of_html_and_add_to_df(html_content)

def scrape_main_func(link, secScroll, categories):
    if link is None:
        link = GRAILED_BASE_URL
    if secScroll is None:
        secScroll = 5
    if categories is None:
        categories = ["all"]

    threads = []

    for cat in categories:
        thread = threading.Thread(target=scrape_html(link, secScroll, cat))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def scrappe_site():
    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument('-link', '--link', type=str, required=False, help='a link to site defoult https://www.grailed.com/categories ')
    parser.add_argument('-secScroll', '--secScroll', type=int, required=False, help='how long to scroll')
    parser.add_argument('-categories', '--categories', type=str, required=False, help='pick categories you want to scrape from ')
    args = parser.parse_args()
    scrape_main_func(args.link, args.secScroll, args.categories)

if __name__ == "__main__":
    scrappe_site()