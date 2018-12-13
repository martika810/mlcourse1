import pickle
import datetime

monthDict={'Jan':1, 'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

with open('ebay_orders.pkl', "rb") as input_file:
    orders = pickle.load(input_file)

for order in orders:

    day = int(order.get('date').split('-')[0])
    month = int(monthDict.get(order.get('date').split('-')[1]))
    year = 2000+int(order.get('date').split('-')[2][:2])
    print(day,month, year)
    week_number = datetime.date(year,month,day).isocalendar()[1]

    print(order.get('date'),week_number)