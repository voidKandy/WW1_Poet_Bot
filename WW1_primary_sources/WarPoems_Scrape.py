import urllib.request
from urllib.request import urlopen
from urllib.error import HTTPError
from fake_useragent import UserAgent
import bs4 as bs
import re
import requests
from tqdm import tqdm
import time

ua = UserAgent()
url = 'https://www.poetryfoundation.org/collections/144683/war-poetry'
# other url = https://www.poetryfoundation.org/collections/101720/world-war-i-poets
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib.request.Request(url, headers=hdr)
sauce = urllib.request.urlopen(req).read()
soup = bs.BeautifulSoup(sauce, 'html.parser')


# Define scrape
def scrape(link):
    url = link
    hdr = {'User-Agent':'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=hdr)
    sauce = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    # Get title and poet
    title = soup.find_all('h1')[0].text
    poet = soup.find_all('a',href=re.compile('.*poets/.*'))[0].text

    # Get poem
    def pretty_text(text):
        final = (((text).replace(u'\xa0', u' ')).replace(u'\r ',u'\n'))
        return final
    poem = (pretty_text(soup.find_all('div', class_="o-poem")[0].text))
    write = poem.replace('\n','')
    #print(write)
    # Define file format
    
    filename = f'{title}-{poet}'
    
    with open(f'warpoems/{filename}.txt','w') as file:
        file.write(write)
        print(f'Printed {title}')

# Parse through div class / p_tags / a_tags
article = soup.find('div', class_='o-article-bd')
print(article)
elements = article.find_all('div', class_='c-feature-cta')
links = [element.find('a')['href'] for element in elements if element.find('a')]
print(links)

# Ready to scrape?
response = input("Poems found, shall I scrape??? (y/n)")
if response == 'y':
    for link in tqdm(links, desc='Scraping', unit='page'):
        try:
            scrape(link)
        except Exception as e:
            print(f"Problem scraping: {link} ERROR: {e}")
            continue
    print('[DONE]')
