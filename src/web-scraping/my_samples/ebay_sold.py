import requests
import json
import re
from bs4 import BeautifulSoup
import dataset
import csv
import pickle
import datetime


def calculate_week_number(date):
    monthDict={'Jan':1, 'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    day = int(date.split('-')[0])
    month = int(monthDict.get(date.split('-')[1]))
    year = 2000+int(date.split('-')[2][:2])
    week_number = datetime.date(year,month,day).isocalendar()[1]
    return week_number

def extract_all_orders(product_id, ebay_product_url):
    session = requests.Session()
    session.headers.update({
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    })
    reply = session.get(ebay_product_url)

    soup = BeautifulSoup(reply.text, 'html.parser')

    buy_now_sold_item_rows = soup.select('body > div.pagewidth > div > div > div > table')[1].select('table')[2].select('tr')

    offer_sold_item_rows = soup.select('body > div.pagewidth > div > div > div > table')[1].select('table')[5].select('tr')

    orders = []

    for item_sold in buy_now_sold_item_rows:
        item_detail_columns = item_sold.findChildren('td')
        if (len(item_detail_columns) > 0): # skip the header column
            orders.append({
                'product_id' : product_id,
                'price' : item_detail_columns[2].text,
                'quantity' : item_detail_columns[3].text,
                'date': item_detail_columns[4].text,
                'week_number': calculate_week_number(item_detail_columns[4].text)
            })



    for item_sold in offer_sold_item_rows:
        item_detail_columns = item_sold.findChildren('td')
        if (len(item_detail_columns) > 0): # skip the header column
            if('Accepted'==item_detail_columns[2].text):
                orders.append({
                    'product_id' : product_id,
                    'price' : '0',
                    'quantity' : item_detail_columns[3].text,
                    'date': item_detail_columns[4].text,
                    'week_number': calculate_week_number(item_detail_columns[4].text)
                })

    return orders

product_ids = [232902350217,232770322170]
orders = []

for product_id in product_ids:

    sold_items_url = 'https://offer.ebay.co.uk/ws/eBayISAPI.dll?ViewBidsLogin&item={}'
    product_url = sold_items_url.format(product_id)
    orders.extend(extract_all_orders(product_id, product_url))


# Save in a file
with open('ebay_orders.pkl','wb') as output_file:
    pickle.dump(orders,output_file)

#Save in excel
with open('ebay_sold.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['product_id', 'price', 'quantity', 'date', 'week_number'])
    for order in orders:
        filewriter.writerow([order.get('product_id'), order.get('price'), order.get('quantity'), order.get('date'), order.get('week_number')])