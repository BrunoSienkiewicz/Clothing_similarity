from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import argparse
import threading
import pandas as pd

"""
flagi = link(defoult ta stronka od ubran), ilesecScroll, kategoria(z multi porcesingiem) 
"""
GRAILED_BASE_URL = "https://www.grailed.com/categories/"

data = {
    'listing_link': [],
    'img_link': [],
    'time_of_scrapping': [],
    'listing_meta_data': [],
    'listing_title': [],
    'listing_price': [],
    'see_similat_link': []
}
df = pd.DataFrame(data)
def init_of_driver(url):
    chrome_options = Options()
    chrome_options.add_argument('--disable-logging')
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    #assert "Grailed" in driver.title
    return driver

def scroll_for_set_amout_of_sec(driver, secScroll):
    end_time = time.time() + secScroll
    while time.time() < end_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)

def bfsoup_parse_of_html_and_add_to_df(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    #print(soup.prettify())
    feed_items = soup.find_all(class_='feed-item')
    for feed_item in feed_items:
        listing_link = feed_item.find('a', class_='listing-item-link')['href']
        print(f'{listing_link} - listing link')
        img_tag = feed_item.find('img', class_='Image-module__crop___nWp1j')
        print(f'img tabgs {img_tag}')
        img_link = [img_tag['src'], img_tag['srcset']]
        print(f'img link - {img_link}')
        time_of_scrapping = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        listing_meta_data = feed_item.find('div', class_='ListingMetadata-module__metadata___+RWy0').text.strip()
        print(f'{listing_meta_data} - listing meta data ')
        listing_title = feed_item.find('p', class_='ListingMetadata-module__title___Rsj55').text.strip()
        print(f"{listing_title} - listing title")
        #listing_price = feed_item.find('span', class_='Money-module__root___jRyq5 Price-module__onSale___1pIHp').text.strip()
        #print(f'{listing_price} - price ')
        see_similar_link = feed_item.find('a', class_='SeeSimilarLink-module__link___tioRk')['href']
        print(f'{see_similar_link}- see_similar_link')


def scrape_html(link, secScroll, categorie):
    cookies_reject_all_id = 'onetrust-reject-all-handler'
    login_widget_xpath = '/html/body/div[9]/div/div/div/div[2]/div'
    random_xpath ='/html/body/div[9]/div'
    url = link + categorie
    driver = init_of_driver(url)
    """
    try:
        reject_button = WebDriverWait(driver, 11).until(EC.element_to_be_clickable((By.ID, cookies_reject_all_id)))
        reject_button.click()
        reject_button.click()
    except Exception as e:
        pass
    """
    #WebDriverWait(driver, 11).until(EC.visibility_of_element_located((By.CLASS_NAME, 'feed-item')))
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
    # Create the parser
    parser = argparse.ArgumentParser(description="A simple script to demonstrate argparse.")

    # Add a flag -f with a required argument
    parser.add_argument('-link', '--link', type=str, required=False, help='a link to site defoult https://www.grailed.com/categories ')
    parser.add_argument('-secScroll', '--secScroll', type=int, required=False, help='how long to scroll')
    parser.add_argument('-categories', '--categories', type=str, required=False, help='pick categories you want to scrape from ')
    args = parser.parse_args()
    scrape_main_func(args.link, args.secScroll, args.categories)


if __name__ == "__main__":
    scrappe_site()