import requests

url = 'http://www.webscrapingfordatascience.com/jsonajax/results2.php'

#r = requests.post(url, data={'api_code': 'C123456'})
r = requests.post(url, json={'api_code': 'C123456'})

print(r.json())
print(r.json().get('results'))