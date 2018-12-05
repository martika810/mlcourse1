import requests

url = ' http://www.webscrapingfordatascience.com/trickylogin/'

my_session = requests.Session()
my_session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'})

r = my_session.post(url)
print(r.request.headers)


r = my_session.post(url,params={'p': 'login'},
                    data={'username': 'dummy', 'password': '1234'})

print(r.request.headers)


r = my_session.get(url ,params={'p': 'protected'})

print(r.request.headers)

print(r.text)