import requests
import json
import re
from bs4 import BeautifulSoup
import dataset

sold_items_url = 'https://offer.ebay.co.uk/ws/eBayISAPI.dll?ViewBidsLogin&item={}'
three_thousand_multicart_sega_id =232902350217
three_thousand_multicart_sega_url = sold_items_url.format(three_thousand_multicart_sega_id)

session = requests.Session()
session.headers.update({
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
})

reply = session.get(three_thousand_multicart_sega_url)

soup = BeautifulSoup(reply.text, 'html.parser')

buy_now_sold_item_rows = soup.select('body > div.pagewidth > div > div > div > table')[1].select('table')[2].select('tr')

offer_sold_item_rows = soup.select('body > div.pagewidth > div > div > div > table')[1].select('table')[5].select('tr')

orders = []


for item_sold in buy_now_sold_item_rows:
    item_detail_columns = item_sold.findChildren('td')
    if (len(item_detail_columns) > 0): # skip the header column
        orders.append({
            'price' : item_detail_columns[2].text,
            'quantity' : item_detail_columns[3].text,
            'date': item_detail_columns[4].text
        })



for item_sold in offer_sold_item_rows:
    item_detail_columns = item_sold.findChildren('td')
    if (len(item_detail_columns) > 0): # skip the header column
        if('Accepted'==item_detail_columns[2].text):
            orders.append({
                'price' : '0',
                'quantity' : item_detail_columns[3].text,
                'date': item_detail_columns[4].text
            })


print(len(orders))
