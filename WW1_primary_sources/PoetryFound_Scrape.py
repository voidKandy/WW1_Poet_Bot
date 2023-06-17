import urllib.request
from urllib.request import urlopen
from urllib.error import HTTPError
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import re
import requests
from tqdm import tqdm
import time

ua = UserAgent()
url = 'https://www.poetryfoundation.org/articles/70139/the-poetry-of-world-war-i'
# other url = https://www.poetryfoundation.org/collections/101720/world-war-i-poets
hdr = {'User-Agent':'Mozilla/5.0'}
req = urllib.request.Request(url, headers=hdr)
sauce = urllib.request.urlopen(req).read()
soup = bs.BeautifulSoup(sauce, 'html.parser')
driver = webdriver.Safari()

# Define scrape
def scrape(page):
    # Go to page with selenium
    driver.get(page)
    time.sleep(2)
    url = driver.current_url
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
    
    with open(f'poems/{filename}.txt','w') as file:
        file.write(write)
        print(f'Printed {title}')

# Parse through div class / p_tags / a_tags
p_tags = soup.find('div', class_='c-userContent').find_all('p')
class_links = [a['href'] for p in p_tags for a in p.find_all('a')]
print(f'{len(class_links)} total links found')

# Filter out links that are not to poems
prefix ='http://www.poetryfoundation.org'
poem_links = [pl for pl in class_links if 'poem' in pl and re.search(r'\d{6}',pl)]
# Add prefixes to pathless poems ;(
for p in poem_links: 
    if prefix not in p:
        newname = prefix + p
        poem_links.remove(p)
        poem_links.append(newname)
print(f'{len(poem_links)} poem links found')
print(poem_links)

# Ready to scrape?
response = input("Poems found, shall I scrape??? (y/n)")
if response == 'y':
    visited = []
    for page in tqdm(poem_links, desc='Scraping', unit = 'page'):
        # prevent duds
        if prefix not in page:
            continue
        # Prevent loops
        if page in visited:
            print("skipping")
            continue
        visited.append(page)
        try:
            scrape(page)
        except Exception as e:
            print(f"Problem scraping: {page}")
            continue
    print('[DONE]')
