import requests
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome('/Users/martarey/dev/python/ml_course1/chromedriver')
driver.implicitly_wait(15)

def extract_all_discount_deals(driver, aliexpress_url):
    driver.get(aliexpress_url)

    content = driver.page_source
    # session = requests.Session()
    # session.headers.update({
    #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    #     'referer': 'https://www.aliexpress.com/'
    # })
    # reply = session.get(aliexpress_url)
    #
    soup = BeautifulSoup(content, 'html.parser')
    price =soup.select('body > div.fd-container > div.fd-main > div.deals-main.container > div > div.deals-list > div div > a > div.item-details > p.current-price')[0].text

    print(price)

extract_all_discount_deals(driver, 'https://flashdeals.aliexpress.com/en.htm?spm=2114.11010108.01002.1.650c649bQ9ue06')

driver.quit()