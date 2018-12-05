from urllib.parse import urljoin

import pandas as pd
from glassdoorscraper import GlassdoorScraper
from databasehelper import DatabaseHelper
from selenium import webdriver


url = 'https://www.glassdoor.co.uk/Reviews/uk-reviews-SRCH_IL.0,2_IN2.htm'
#url = 'https://www.glassdoor.co.uk/Reviews/uk-reviews-SRCH_IL.0,2_IN2_IP5210.htm'

driver = webdriver.Chrome('/Users/martarey/dev/python/ml_course1/src/web-scraping/chromedriver')
driver.implicitly_wait(15)

glassdoor_scraper = GlassdoorScraper(driver)
database_helper = DatabaseHelper()
database_helper.create_schema()
start_page_url =database_helper.get_random_unvisited_link()
if(start_page_url is None):
    start_page_url = 'https://www.glassdoor.co.uk/Reviews/uk-reviews-SRCH_IL.0,2_IN2.htm'
driver.get(start_page_url)
database_helper.store_link(start_page_url)
database_helper.mark_visited(start_page_url)

isLastPage=glassdoor_scraper.is_last_page(driver)
#print(is_last_page)
links_to_visit = []
company_dataframe = pd.DataFrame()
count = 0
while(not isLastPage):
    # Open page and load information
    next_button = driver.find_element_by_css_selector('#FooterPageNav li.next a')
    next_url = glassdoor_scraper.get_next_page(driver,url)
    driver.get(next_url)
    list_companies = glassdoor_scraper.list_companies_in_current_page(driver)
    for company in list_companies:
        company_dataframe=company_dataframe.append(pd.Series(company),ignore_index=True)

    database_helper.store_link(driver.current_url)
    database_helper.mark_visited(driver.current_url)
    links_to_visit.append(next_url)
    #print(next_url)
    isLastPage=glassdoor_scraper.is_last_page(driver)

    #append rows
    with open('uk_companies_data.csv', 'a') as f:
        company_dataframe.to_csv(f,header=False)


print(links_to_visit)
driver.quit()
    #FooterPageNav > div > ul > li.next > span.disabled
    #FooterPageNav > div > ul > li.next > a
    #MainCol > div:nth-child(1) > div:nth-child(3)
    #MainCol > div:nth-child(1) > div:nth-child(3) > div.empInfo.tbl > div.header.cell.info > div.margBotXs > a
    #MainCol > div:nth-child(1) > div:nth-child(3) > div.empLinks.tbl.noswipe > span > div > span:nth-child(1) > span.bigRating.strong.margRtSm.h1

