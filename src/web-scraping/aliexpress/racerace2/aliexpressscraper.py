from selenium import webdriver
import pickle
from categoryscraper import CategoryScraper


def get_cookies(browser):
    browser.get("https://login.aliexpress.com/buyer.htm?return=https%3A%2F%2Fwww.aliexpress.com%2F&random=CEA73DF4D81D4775227F78080B9B6126")
    print('input your username and password in Firefox and hit Submit')
    input('Hit Enter here if you have summited the form: <Enter>')
    cookies = browser.get_cookies()
    pickle.dump(cookies, open("cookies.pickle", "wb"))


def set_cookies(browser,url):
    browser.get(url)
    cookies = pickle.load(open("cookies.pickle", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.add_cookie({'name':'aep_usuc_f',
                        'value':'isfm=y&site=glo&c_tp=GBP&x_alimid=814979923&isb=y&ups_u_t=1577293226431&region=UK&b_locale=en_US&ae_u_p_s=0'})
    browser.get(url)


browser = webdriver.Chrome('/Users/martarey/dev/python/ml_course1/chromedriver')

browser.implicitly_wait(15)
get_cookies(browser)
home_decoration_url = 'https://www.aliexpress.com/store/group/Custom-made-Wall-Stickers/1225042_259917284/31.html?spm=2114.12010612.8148361.10.626f6048YIxtUz&origin=n&SortType=bestmatch_sort&g=y'
other_stickers_url = 'https://aliexpress.com/store/group/wall-sticker/1240606_255836737.html?spm=2114.12010612.8148362.8.4a527014lfiHPA&origin=n&SortType=price_asc&g=y'
set_cookies(browser, home_decoration_url)


categoty_scraper = CategoryScraper(browser)
categoty_scraper.scrape(home_decoration_url, 'test1.csv')
categoty_scraper.scrape(other_stickers_url, 'test2.csv')

browser.quit()

