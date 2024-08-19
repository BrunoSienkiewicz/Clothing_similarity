import time
import argparse
import threading
import json
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FireOptions
from bs4 import BeautifulSoup

GRAILED_BASE_URL = "https://www.grailed.com/categories/"
GRAILED_HOME_URL = "https://www.grailed.com"

def init_driver(url):
    options = FireOptions()
    options.add_argument('--disable-logging')
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = webdriver.Firefox(options)
    driver.get(url)
    return driver

def scroll_for_set_amout_of_sec(driver, scroll_time, timeout=0.1):
    end_time = time.time() + scroll_time
    while time.time() < end_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    feed_items = soup.find_all(class_='feed-item')
    iteration = 0
    json_array = []
    for feed_item in feed_items:
            saved_links = {}
            iteration += 1
            try:
                feed_item.find('a', class_='listing-item-link')['href']
            except TypeError:
                break
            saved_links['listing_link'] = GRAILED_HOME_URL + feed_item.find('a', class_='listing-item-link')['href']
            saved_links['img_link'] = re.sub(r'\?.*$', '', feed_item.find('img', class_='Image-module__crop___nWp1j')['src'])
            saved_links['similar_link'] = GRAILED_BASE_URL + feed_item.find('a', class_='SeeSimilarLink-module__link___tioRk')['href']
            saved_links['time_of_scrapping'] = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            json_array.append(save_to_json_file(saved_links))
    return json_array


def save_to_json_file(saved_links):
    return json.dump(saved_links, indent=4)

def save_to_folder(json_file, filename, folder_name='json_dataset'):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, filename)
    with open(folder_name, 'W') as file:
        file.write(json_file)
    print(f"File saved successfully at {file_path}")

def scrape_html(link=GRAILED_BASE_URL, sec_scroll=5, timeout=0.1, categorie="all"):
    url = link + categorie
    driver = init_driver(url)
    scroll_for_set_amout_of_sec(driver, sec_scroll, timeout)
    parent_element = driver.find_element(By.CLASS_NAME, "feed")
    html_content = parent_element.get_attribute('outerHTML')
    driver.close()
    return parse_html(html_content)

def main_func_for_users(link, sec_scroll,timeout, categories):
    json_array = scrape_html(link, sec_scroll, timeout, categories)
    x = 0
    for json in json_array:
        x += 1
        save_to_folder(json, f"json_file_nr{x}")

def main():
    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")
    parser.add_argument('-link', '--link', type=str, const=GRAILED_BASE_URL, required=False, help='a link to site defoult https://www.grailed.com/categories ')
    parser.add_argument('-sec_scroll', '--secScroll', type=int, const=5, required=False, help='how long to scroll')
    parser.add_argument('-timeout', '--timeout', type=float, const=0.1, required=False, help='how long to timeout scroll')
    parser.add_argument('-categories', '--categories', type=str, const='all', required=False, help='pick categories you want to scrape from ')
    args = parser.parse_args()
    main_func_for_users(args.link, args.sec_scroll,args.timeout, args.categories)

