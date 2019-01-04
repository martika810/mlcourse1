import pandas as pd
from selenium import webdriver
import pickle
import time
from bs4 import BeautifulSoup
import pandas as pd


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

def extract_product_data(product_html_page):
    product_dict = {}
    html_parser = BeautifulSoup(product_html_page, 'html.parser')
    images = html_parser.select('#j-image-thumb-list > li > span > img')
    images_values = ''
    for image in images:
        images_values = images_values + ';' + image.get_attribute_list('src')[0]
    # images.get_attribute('src')
    product_dict['images'] = images_values[1:]
    title = html_parser.select('#j-product-detail-bd div.store-detail-main div h1.product-name')[0].text
    product_dict['title'] = title
    # price
    currency = html_parser.select('#j-product-detail-bd > div.store-detail-main div.product-price > div > div.p-price-detail.util-clearfix > div > div > span.p-symbol')[0].text
    prices = html_parser.select('#j-sku-discount-price > span')
    if(len(prices)>0):
        first_price = prices[0].text
        second_price = prices[1].text
        product_dict['price'] = currency+''+first_price+'-'+second_price
    else:
        first_price = html_parser.select('#j-sku-discount-price')[0].text
        product_dict['price'] = currency+' '+first_price

    #attributes
    attributes = html_parser.select('#j-product-info-sku > dl.p-property-item')
    number_attributes = len(attributes)
    for attribute in attributes:
        title = attribute.select('dt.p-item-title')[0].text[:-1]
        values_list =attribute.select('dd.p-item-main li span')
        values = ''
        for attribute_value in values_list:
            values = values + ';' + attribute_value.text
        product_dict[title] = values[1:]
    #specifications
    specification_list = html_parser.select('#j-product-desc div.ui-box-body > ul.product-property-list li')
    for specification_item in specification_list:
        title = specification_item.select('.propery-title')[0].text[:-1]
        description = specification_item.select('.propery-des')[0].text
        product_dict[title] = description

    return product_dict

def crawling_to_findall_pages(browser,url_pattern):

    allproducts = []
    initial_url = url_pattern.replace('{page}','1')
    fullpage = browser.get(initial_url)
    browser.find_element_by_css_selector('#nav-global > div.ng-item.ng-goto-globalsite > a').click()
    browser.get(initial_url)
    html_full_page = browser.page_source
    html_soup_parser = BeautifulSoup(html_full_page, 'html.parser')
    all_products_loaded_in_beatifulsoup = html_soup_parser.find_all('a', class_='pic-rind')
    print('allproducts loaded by beautiful: {}'.format(len(all_products_loaded_in_beatifulsoup)))
    end_arrow = browser.find_element_by_xpath('//*[@id="pagination-bottom"]/div[1]/a[10]')
    total_number_pages = int(end_arrow.text)

    next_button = browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
    isLastPage = next_button.get_attribute('class').find('disabled')>-1
    dataframe = pd.DataFrame()
    while not isLastPage:


        for product_index in range(1,len(all_products_loaded_in_beatifulsoup)+1):
            all_product_pages = browser.find_elements_by_css_selector('a.pic-rind')
            #product_url = all_products_loaded_in_beatifulsoup[product_index-1].get_attribute('href')
            #allproducts.append(product_url)
            all_product_pages[product_index-1].click()
            time.sleep(5)
            product_html_page = browser.page_source
            product_data = extract_product_data(product_html_page)
            if(product_index == 1):
                dataframe = dataframe.append(pd.Series(product_data,index= product_data.keys()),ignore_index=True)
            else:
                dataframe = dataframe.append(pd.Series(product_data,index= product_data.keys()),ignore_index=True)
            browser.back()

        next_button = browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
        next_button.click()
        time.sleep(2)
        next_button = browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
        isLastPage = next_button.get_attribute('class').find('disabled')>-1
        dataframe.to_excel('products2.xlsx')

    
    return allproducts

# do web crawling to extract all links
# for each page extract all product links
# extract the data for each product link

initial_url_pattern = 'https://aliexpress.com/store/group/wall-sticker/1240606_255836737.html'
#url = 'https://www.glassdoor.co.uk/Reviews/uk-reviews-SRCH_IL.0,2_IN2_IP5210.htm'
#try:
browser = webdriver.Chrome('/Users/martarey/dev/python/ml_course1/chromedriver')
browser.implicitly_wait(15)
get_cookies(browser)

initial_url = initial_url_pattern.replace('{page}','')
set_cookies(browser, initial_url)

all_products = crawling_to_findall_pages(browser,initial_url_pattern)

print(len(all_products))

browser.quit()
# except Exception as e:
#     browser.quit()
#     print(str(e))

