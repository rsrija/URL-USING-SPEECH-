import urllib.request
import bs4 as bs
url="https://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=blue+shirts+men"
htmlfile = urllib.request.urlopen(url)
htmltext = htmlfile.read()
links = []
a=[]
soup=bs.BeautifulSoup(htmltext,'lxml')
all_tables=soup.find_all('li',  {'class': 'a-link-normal a-text-normal'})
for link in soup.find_all('li'):
    links.append(link.get('data-asin'))
print (set(links))
links= (set(links))



