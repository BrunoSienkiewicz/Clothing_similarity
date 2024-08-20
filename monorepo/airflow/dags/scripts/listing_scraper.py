import json
import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FireOptions
from selenium.webdriver.common.by import By


css_classes = {
    'headline': 'Headline_headline___qUL5 Text Details_designers__NnQ20',
    'details_title': 'Body_body__dIg1V Text Details_title__PpX5v',
    'p_elements': 'Body_body__dIg1V Text Details_detail__J0Uny Details_nonMobile__AObqX',
    'price': 'Money_root__8lDCT',
    'tags': 'Hashtags_tags__CwSY4'
}

def init_driver(url):
    options = FireOptions()
    options.add_argument('--disable-logging')
    options.add_argument('--headless')
    options.add_argument("--log-level=3")

    driver = webdriver.Firefox(options=options)
    driver.get(url)
    return driver


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed_listing = {}
    #parsed_listing['headline'] = soup.find('p', class_='Headline_headline___qUL5 Text Details_designers__NnQ20').text
    parsed_listing['headline'] = [item.strip() for item in soup.find('p', class_=css_classes['headline']).text.split('×') if item.strip()]
    parsed_listing['details_title'] = soup.find('h1', class_=css_classes['details_title']).text

    details_p_elements = soup.find_all('p', class_=css_classes['p_elements'])
    parsed_listing['size'] = details_p_elements[0].text[5:]
    parsed_listing['Color'] = details_p_elements[1].text[6:]
    parsed_listing['Condition'] = details_p_elements[2].text[10:]

    parsed_listing['price'] = soup.find('span', class_=css_classes['price']).text

    parsed_listing['tags'] = soup.find('div', class_=css_classes['tags']).text.replace('#', ' #').strip().split(' ')

    return parsed_listing


def save_info(parsed_listing, img_link, folder_path='parsed_json_dataset'):
    save_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    save_parsed_json(parsed_listing, save_time, folder_path)
    save_image(img_link, save_time, folder_path)


def save_image(img_link, save_time, folder_path):
    response = requests.get(img_link)

    if response.status_code == 200:
        filename = f"{save_time}.png"
        image_path = os.path.join(folder_path, filename)
        with open(image_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Failed to save image. {response.status_code}')


def save_parsed_json(parsed_listing, save_time, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{save_time}.json"
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as f:
        json.dump(parsed_listing, f, indent=4)

def scrape_html(url):
    driver = init_driver(url)
    parent_element = driver.find_element(By.CLASS_NAME, 'MainContent_sidebar__29G6s')
    html_content = parent_element.get_attribute('outerHTML')
    driver.quit()
    return parse_html(html_content)

def get_listing():
    with open("json_dataset/2024-08-07 22-14-37_nr93.json", 'r') as f:
        listing = json.load(f)
        return listing


def main():
    listing = get_listing()
    parsed_listing = scrape_html(listing["listing_link"])
    save_info(parsed_listing, listing["img_link"])


if __name__ == "__main__":
    main()
