from bs4 import BeautifulSoup, SoupStrainer
import urllib
import requests
import csv

def urlclean(url):
    p = urllib.parse.urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc

    p = urllib.parse.ParseResult('http', netloc, path, *p[3:])
    return p.geturl()

# url = "http://www.mindmusclenutrition.com"
# url = urlclean(url)

def getIGfollowers(clean_url):
    page = requests.get(clean_url)    
    data = page.text
    soup = BeautifulSoup(data)

    for link in soup.find_all('a'):
        if 'instagram' in str(link.get('href')):
            print(link.get('href'))
            url = link.get('href')
            r = requests.get(url).text
            start = '"edge_followed_by":{"count":'
            end = '},"followed_by_viewer"'

            follower_count = r[r.find(start)+len(start):r.rfind(end)]
        else:
            continue

    return follower_count

with open('url_bulk.csv', 'r') as open_file:
    f = csv.writer(open('url_bulk_with_followers.csv', "w"))

    for row in csv.reader(open_file):
        # print(row[0])
        url = urlclean(row[0])
        print(url)
        try:
            followers = getIGfollowers(url)
        except:
            followers = 'N/A'
        print(followers)
        f.writerow([row[0],
                followers])

