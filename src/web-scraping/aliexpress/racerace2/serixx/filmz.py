#!/usr/bin/python
# coding: UTF-8
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding':'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '__cfduid=dd576e0c131f7c5da8e282e089f22e9561535580186; _ga=GA1.2.984662716.1535584256; _gid=GA1.2.542920819.1535584256; cf_clearance=9d19c5045f16b931f8ceaa229dc5d6ae786301ef-1536254257-1800-150; csrf_cookie_name=ab7a5d4e092d01f074d5668475ddd991; ci_session=5994770b829598aba493adaa4fad867bbafe00b5; __atuvc=22%7C36; __atuvs=5b9161385c585bd2000; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Fwww3.tfarjo.ws%2Fserie%2Fbetter-call-saul%2F%22%2C%22svsds%22%3A5%2C%22TejndEEDj%22%3A%22V2PVDLAzF%22%7D%2C%22C230427%22%3A%7B%22page%22%3A1%2C%22time%22%3A1536254266991%7D%2C%22C230428%22%3A%7B%22page%22%3A1%2C%22time%22%3A1536254267115%7D%7D',
    'referer': 'https://www.filmz.cc/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

HEADERS2 = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import requests, os, sys, time
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import simplejson
import json
import re
from decimal import *


def collectLinks(lnk, fl, code):
    if (code == 3):
        pg = 0
        counter = 0
        arr = []
        while (True):
            print("[{0}][{1}] Load urls".format(counter, pg / 16))
            req = requests.get(lnk + (str)(pg), headers=HEADERS)
            # print req.text.encode('utf8')
            tree = html.fromstring(req.text.decode('utf8'))
            aLinks = tree.xpath("//li/div[@class='image']/a[1]/@href")
            # soup = BeautifulSoup(req.text, 'html.parser')
            # print aLinks
            # aLinks = soup.find_all('a', class_='ml-mask')
            if (len)(aLinks) == 0: return arr

            for aLink in aLinks:
                aLink = re.findall(r"([^>]*)saison", aLink)
                try:
                    aLink = aLink[0]
                    arr.append(aLink)
                    counter += 1
                except:
                    continue

            f = open(fl, "a")
            f.write("\n".join(arr) + "\n")
            f.close()

            pg += 16
            # break
    else:
        pg = 0
        counter = 0
        arr = []
        while (True):
            print("[{0}][{1}] Load urls".format(counter, pg / 16))
            req = requests.get(lnk + (str)(pg), headers=HEADERS)
            tree = html.fromstring(req.text.decode('utf8'))
            aLinks = tree.xpath("//li/div[@class='image']/a[1]/@href")
            # soup = BeautifulSoup(req.text, 'html.parser')

            # aLinks = soup.find_all('a', class_='ml-mask')
            if (len)(aLinks) == 0: return arr

            for aLink in aLinks:
                # print aLink
                try:
                    arr.append(aLink)
                    counter += 1
                except:
                    continue

            f = open(fl, "a")
            f.write("\n".join(arr) + "\n")
            f.close()

            pg += 16
            # break


def loadEmbed(csrf_name, movies, lnk, code):
    if (code == 2):
        headersPost = {
            'accept': '*/*',
            # 'accept-encoding':'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            # 'content-length':'66',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '__cfduid=dd576e0c131f7c5da8e282e089f22e9561535580186; _ga=GA1.2.984662716.1535584256; _gid=GA1.2.542920819.1535584256; cf_clearance=9d19c5045f16b931f8ceaa229dc5d6ae786301ef-1536254257-1800-150; csrf_cookie_name=ab7a5d4e092d01f074d5668475ddd991; ci_session=5994770b829598aba493adaa4fad867bbafe00b5; __atuvc=22%7C36; __atuvs=5b9161385c585bd2000; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Fwww3.tfarjo.ws%2Fserie%2Fbetter-call-saul%2F%22%2C%22svsds%22%3A5%2C%22TejndEEDj%22%3A%22V2PVDLAzF%22%7D%2C%22C230427%22%3A%7B%22page%22%3A1%2C%22time%22%3A1536254266991%7D%2C%22C230428%22%3A%7B%22page%22%3A1%2C%22time%22%3A1536254267115%7D%7D',
            # 'cookie':'__cfduid=dceb03a21d7efd7c400ba5f9fd5cd599e1532636537; _ga=GA1.2.783431858.1532636546; _gid=GA1.2.1907221562.1533770019; _PN_SBSCRBR_FALLBACK_DENIED=1; __test; csrf_cookie_name='+csrf_name+'; ci_session=77e84855174e1f905a845c6e66b4185801c0ab43; _gat=1; __atuvc=17%7C32; __atuvs=5b6cb337a8d3274b002; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A34%2C%22TejndEEDj%22%3A%22r8aFva49%22%7D%2C%22C230427%22%3A%7B%22page%22%3A2%2C%22time%22%3A1533851908215%7D%2C%22C230428%22%3A%7B%22page%22%3A2%2C%22time%22%3A1533851909192%7D%7D',
            'origin': 'https://www.filmz.cc/',
            'referer': lnk,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        datas = {'csrf_test_name': csrf_name,
                 'movie': movies}
        zhao = requests.post('https://www.filmz.cc/getlink', data=datas, headers=headersPost)
        jsonLoad = simplejson.loads(zhao.content)
        tree2 = html.fromstring(jsonLoad['iframe'])
        hahay = tree2.xpath("//*/@src")

        return hahay[0]
    elif (code == 3):
        headersPost = {
            'accept': '*/*',
            # 'accept-encoding':'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            # 'content-length':'66',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '__cfduid=dd576e0c131f7c5da8e282e089f22e9561535580186; _ga=GA1.2.984662716.1535584256; _gid=GA1.2.542920819.1535584256; cf_clearance=9d19c5045f16b931f8ceaa229dc5d6ae786301ef-1536254257-1800-150; csrf_cookie_name=ab7a5d4e092d01f074d5668475ddd991; ci_session=5994770b829598aba493adaa4fad867bbafe00b5; __atuvc=22%7C36; __atuvs=5b9161385c585bd2000; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Fwww3.tfarjo.ws%2Fserie%2Fbetter-call-saul%2F%22%2C%22svsds%22%3A5%2C%22TejndEEDj%22%3A%22V2PVDLAzF%22%7D%2C%22C230427%22%3A%7B%22page%22%3A1%2C%22time%22%3A1536254266991%7D%2C%22C230428%22%3A%7B%22page%22%3A1%2C%22time%22%3A1536254267115%7D%7D',
            # 'cookie':'__cfduid=dceb03a21d7efd7c400ba5f9fd5cd599e1532636537; _ga=GA1.2.783431858.1532636546; _gid=GA1.2.1907221562.1533770019; _PN_SBSCRBR_FALLBACK_DENIED=1; __test; csrf_cookie_name='+csrf_name+'; ci_session=77e84855174e1f905a845c6e66b4185801c0ab43; _gat=1; __atuvc=17%7C32; __atuvs=5b6cb337a8d3274b002; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A34%2C%22TejndEEDj%22%3A%22r8aFva49%22%7D%2C%22C230427%22%3A%7B%22page%22%3A2%2C%22time%22%3A1533851908215%7D%2C%22C230428%22%3A%7B%22page%22%3A2%2C%22time%22%3A1533851909192%7D%7D',
            'origin': 'https://www.filmz.cc/',
            # 'referer':lnk,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        datas = {'csrf_test_name': csrf_name,
                 'episode': movies}
        zhao = requests.post('https://www.filmz.cc/getlinke', data=datas, headers=headersPost)
        jsonLoad = simplejson.loads(zhao.content)
        tree2 = html.fromstring(jsonLoad['iframe'])
        hahay = tree2.xpath("//*/@src")

        return hahay[0]


# Requests Functions
def getImdb(title):
    try:
        req = requests.get('https://www.imdb.com/find?q={0}'.format(title), headers=HEADERS2)
        soup = BeautifulSoup(req.text, 'html.parser')
        result = soup.find('td', class_='result_text')
        url = result.find('a')
        return url['href'].split('/')[-2]
    except Exception as e:
        # print (str)(e)
        return ''


def getTmdb(title):
    try:
        req = requests.get('https://www.themoviedb.org/search?query={0}'.format(title), headers=HEADERS2)
        soup = BeautifulSoup(req.text, 'html.parser')
        result = soup.find('a', class_='title result')
        return result['href'].split('/')[-1]
    except Exception as e:
        # print (str)(e)
        return ''


# Files Functions ===================================================
def fileExist(f):
    if os.path.isfile(f):
        return True
    else:
        return False


def readFile(filename):
    array = []
    if not fileExist(filename): return array
    with open(filename) as f:
        for line in f:
            array.append(line.replace("\n", "").strip())
        f.close()

    return array


# Arguments
if (len)(sys.argv) != 2:
    print("Usage: {0} <movies|tvshows|episode>".format(sys.argv[0]))
    sys.exit(1)
else:
    TYPE = sys.argv[1]

# Main
try:
    if TYPE == 'episode':
        if not fileExist('episode.txt'): collectLinks('https://www.filmz.cc/series/page/', 'episode.txt', 2)
        tmp = list(set(readFile('episode.txt')))

        # check csv
        arr = []
        if fileExist('episode.csv'):
            csv = readFile('episode.csv')
            db = []
            for r in csv: db.append(r.split(',')[-1])
            for r in tmp:
                if r not in db: arr.append(r)
        else:
            arr = tmp
        countah = 1
        print("{0}/{1} Result(s) Found".format((len)(arr), (len)(tmp)))
    for i, lnk in enumerate(arr):
        srcs = []

        req = requests.get(lnk, headers=HEADERS)
        # print lnk
        tree = html.fromstring(req.text.decode('utf8'))

        # title = tree.xpath("//span[@class='ltype']/text()")
        # title = title[1]
    try:
        title = tree.xpath("//*[@property='og:title']/@content")
        title = re.findall(r"([^>]*) saison", title[0])
        title = title[0]
    except:
        try:
            title = tree.xpath("//span[@class='ltype']/text()")
            title = title[1]
        except:
            pass
    # title = title[1]
    # print "loading.. " + title
    # print ""
    # get imdb & tmdb
imdb = getImdb(title)
tmdb = getTmdb(title)
if (len)(tmdb) == 0:
    pass

try:
    episode = re.findall(r"episode-(.*?)-", lnk)
    episode = (int)(episode[0])
except:
    try:
        episode = re.findall(r"episode-([^>]*)", lnk)
        episode = (int)(episode[0])
    except:
        episode = 0
# print episode
try:
    season = re.findall(r"saison-(.*?)\/", lnk)
    season = (int)(season[0])
except:
    season = 0

csrf_name = tree.xpath("//*[@id='csrf_test_name']/@value")
csrf_name = csrf_name[0]
try:
    movies_code = tree.xpath("//button[contains(@class,'player') and contains(.,'openload')]/@onclick")
    if (len(movies_code) > 0):
        movies_code = movies_code[0]

        movies = re.findall(r"'(.*)'", movies_code)
        movies = movies[0]

        srcs.append(loadEmbed(csrf_name, movies, lnk, 3))
except:
    pass

try:
    movies_code = tree.xpath("//button[contains(@class,'player') and contains(.,'streamango')]/@onclick")
    if (len(movies_code) > 0):
        movies_code = movies_code[0]

        movies = re.findall(r"'(.*)'", movies_code)
        movies = movies[0]

        srcs.append(loadEmbed(csrf_name, movies, lnk, 3))
except:
    pass
# sys.stdout.write('.')
print
"%.3f " % (float(float(countah * 100) / float(len(arr)))) + " % "
countah = countah + 1
# write file
f = open('episode.csv', 'a')
f.write(imdb + ',' + tmdb + ',' + (str)(season) + ',' + (str)(episode) + ',' + '|'.join(srcs) + ',' + lnk + '\n')
f.close()

elif TYPE == 'movies':
if not fileExist('movies.txt'): collectLinks('https://www.filmz.cc/films/page/', 'movies.txt', 2)
tmp = list(set(readFile('movies.txt')))

# check csv
arr = []
if fileExist('movies.csv'):
    csv = readFile('movies.csv')
    db = []
    for r in csv: db.append(r.split(',')[-1])
    for r in tmp:
        if r not in db: arr.append(r)
else:
    arr = tmp

print("{0}/{1} Result(s) Found".format((len)(arr), (len)(tmp)))
countah = 1
for i, lnk in enumerate(arr):
    links = []
    srcs = []

    req = requests.get(lnk, headers=HEADERS)
    tree = html.fromstring(req.text.decode('utf8'))
    title = tree.xpath("//h3[contains(@class,'movie')]/span/text()")
    title = title[0]
    csrf_name = tree.xpath("//*[@id='csrf_test_name']/@value")
    csrf_name = csrf_name[0]
    try:
        movies_code = tree.xpath("//button[contains(@class,'player') and contains(.,'openload')]/@onclick")
        if (len(movies_code) > 0):
            movies_code = movies_code[0]

            movies = re.findall(r"'(.*)'", movies_code)
            movies = movies[0]

            srcs.append(loadEmbed(csrf_name, movies, lnk, 2))
    except:
        continue

    try:
        movies_code = tree.xpath("//button[contains(@class,'player') and contains(.,'streamango')]/@onclick")
        if (len(movies_code) > 0):
            movies_code = movies_code[0]

            movies = re.findall(r"'(.*)'", movies_code)
            movies = movies[0]

            srcs.append(loadEmbed(csrf_name, movies, lnk, 2))
    except:
        continue

    # get imdb & tmdb
    srcs = list(set(srcs))
    imdb = getImdb(title)
    tmdb = getTmdb(title)
    if (len)(imdb) == 0: continue
    print
    "%.3f " % (float(float(countah * 100) / float(len(arr)))) + " % "
    countah = countah + 1
    # write file
    f = open('movies.csv', 'a')
    f.write(imdb + ',' + tmdb + ',' + '|'.join(srcs) + ',' + lnk + '\n')
    f.close()

else:
    if not fileExist('tvshows.txt'): collectLinks('https://www.filmz.cc/series/page/', 'tvshows.txt', 3)
        tmp = list(set(readFile('tvshows.txt')))

    # check csv
arr = []
if fileExist('tvshows.csv'):
    csv = readFile('tvshows.csv')
    db = []
    for r in csv: db.append(r.split(',')[-1])
    for r in tmp:
        if r not in db: arr.append(r)
else:
    arr = tmp

print("{0}/{1} Result(s) Found".format((len)(arr), (len)(tmp)))

countah = 1

for i, lnk in enumerate(arr):

    req = requests.get(lnk, headers=HEADERS)
    # print req.text.encode('utf8')
    print
    lnk
    tree = html.fromstring(req.text.decode('utf8'))

    try:
        title = tree.xpath("//*[@property='og:title']/@content")
        title = re.findall(r"([^>]*) streaming", title[0])
        title = title[0]
    except:
        try:
            title = tree.xpath("//span[@class='ltype']/text()")
            title = title[1]
        except:
            pass
    print
    title
    print
    "## load - " + title + " ##"
    # get imdb & tmdb
    imdb = getImdb(title)
    tmdb = getTmdb(title)
    if (len)(tmdb) == 0: continue

    eps = tree.xpath("//div[@class='panel-body']/a/@href")
    # print eps

    print
    "%.3f " % (float(float(countah * 100) / float(len(arr)))) + " % "
    countah = countah + 1

    for ep in eps:
        srcs = []
        # print ep
        try:
            episode = re.findall(r"episode-(.*?)-", ep)
            episode = (int)(episode[0])
        except:
            try:
                episode = re.findall(r"episode-([^>]*)", ep)
                episode = (int)(episode[0])
            except:
                episode = 0
        # print episode
        try:
            season = re.findall(r"saison-(.*?)\/", ep)
            season = (int)(season[0])
        except:
            season = 0

        req = requests.get(ep, headers=HEADERS)
        tree = html.fromstring(req.text.decode('utf8'))
        csrf_name = tree.xpath("//*[@id='csrf_test_name']/@value")
        csrf_name = csrf_name[0]

        try:
            movies_code = tree.xpath("//button[contains(@class,'player') and contains(.,'openload')]/@onclick")
            if (len(movies_code) > 0):
                movies_code = movies_code[0]

                movies = re.findall(r"'(.*)'", movies_code)
                movies = movies[0]

                srcs.append(loadEmbed(csrf_name, movies, lnk, 3))
        except:
            print
            ""

        try:
            movies_code = tree.xpath("//button[contains(@class,'player') and contains(.,'streamango')]/@onclick")
            if (len(movies_code) > 0):
                movies_code = movies_code[0]

                movies = re.findall(r"'(.*)'", movies_code)
                movies = movies[0]
                # print movies
                srcs.append(loadEmbed(csrf_name, movies, lnk, 3))
                # print loadEmbed(csrf_name,movies)
        except:
            print
            ""

        print("{0}/{1} {2}: Season {3} Episode {4}".format(i + 1, (len)(arr), title, season, episode))
        # sys.stdout.write('.')
        f = open('tvshows.csv', 'a')
        f.write(
            imdb + ',' + tmdb + ',' + (str)(season) + ',' + (str)(episode) + ',' + '|'.join(srcs) + ',' + lnk + '\n')
        f.close()


except KeyboardInterrupt :
    print("\nScript terminated by the user.")
