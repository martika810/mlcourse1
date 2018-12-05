from urllib.parse import urljoin

class CompanyData:
    def __init__(self,name,score,num_reviews):
        self.name=name
        self.score=score
        self.num_reviews=num_reviews

class GlassdoorScraper:
    def __init__(self,driver):
        self.driver = driver

    def extract_company_info(self,panel_company):
        try:
            company_title = panel_company.find_element_by_css_selector('div.margBotXs > a')
            score_company = panel_company.find_element_by_css_selector('span.bigRating.strong.margRtSm.h1')
            number_reviews = panel_company.find_element_by_css_selector('a.eiCell.cell.reviews > span.num.h2')
            return CompanyData(company_title.text,score_company.text,number_reviews.text)
        except:
            print('Error reading company %s'.format(company_title))
            return CompanyData(company_title.text,None,None)

    def list_companies_in_current_page(self,driver):
        companies_found = []
        for panel_company in driver.find_elements_by_css_selector('#MainCol div.eiHdrModule'):
            company_data=self.extract_company_info(panel_company)
            companies_found.append(company_data)
        return companies_found

    def is_last_page(self,driver):
        next_button = driver.find_element_by_css_selector('#FooterPageNav li.next span')
        next_button_classes=next_button.get_attribute("class")
        return next_button_classes == 'disabled'

    def get_next_page(self,driver,url):
        ##FooterPageNav > div > ul > li.next > a
        next_button = driver.find_element_by_css_selector('#FooterPageNav li.next a')
        next_url_link = next_button.get_attribute('href')
        next_full_link = urljoin(url,next_url_link)
        return next_full_link
