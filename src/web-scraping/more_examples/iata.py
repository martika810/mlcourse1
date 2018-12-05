import pandas
import requests
from bs4 import BeautifulSoup

url = 'http://www.iata.org/publications/Pages/code-search.aspx'

def get_results(airline_name):

    session = requests.Session()
    # Spoof the user agent as a precaution
    session.headers.update({
        'X-MicrosoftAjax'  : 'Delta=true',
        'X-Requested-With' : 'XMLHttpRequest',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    })

    # Get the search page
    r = session.get(url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    form = html_soup.find(id='aspnetForm')

    # Get the form fields
    data = {}
    for inp in form.find_all(['input', 'select']):
        name = inp.get('name')
        value = inp.get('value')
        if not name:
            continue
        if 'ddlImLookingFor' in name:
            data[name] = 'ByAirlineName'
        # Airline name
        if 'txtSearchCriteria' in name:
            data[name] = airline_name


    # Perform a POST
    r = session.post(url, data=data)
    print(r.text)
    html_soup = BeautifulSoup(r.text,"html.parser")
    table = html_soup.find('table', class_="datatable")
    df=pandas.read_html(str(table))
    return df
airline_dataframe = get_results('Lufthansa')
print(airline_dataframe)