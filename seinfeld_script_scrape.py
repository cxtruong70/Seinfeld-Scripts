import csv
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Setup domain
url = 'https://www.seinfeldscripts.com/seinfeld-scripts.html'
root = 'https://www.seinfeldscripts.com/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
source = requests.get(url, headers=headers).text

# Run beautiful soup, get list of individual episode scripts
soup = BeautifulSoup(source,'lxml')
tables = soup.find_all('table')
link_table = tables[1]
df = pd.read_html(str(link_table))
episode_links = link_table.find_all('a')
episode_links

# Clean -- Unwrap href tags, remove extra spaces
link_strings = [x['href'] for x in episode_links]
cleaned_strings = [x.replace(' ', '') for x in link_strings]

# Check cleaning results
cleaned_strings[0]

# Request the html, and generate the soup for that page
def request_html(url):
    
    root = 'https://www.seinfeldscripts.com/'
    url = root + url
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    source = requests.get(url, headers=headers).text 
    soup = BeautifulSoup(source,'lxml')
    
    time.sleep(2)
    return soup

# Go through soup p_tags, extract test, return entire script
def extract_text(p_tags):
    temp = ''
    for tag in p_tags:
        text = tag.get_text()
        temp = temp + text
    return temp

# Count phrases per script
def count_phrase(phrase,df):
    counts = []
    for e,row in df.iterrows():
        scrpt = row.scripts
        count = scrpt.count(phrase)
        counts.append(count)
    df[phrase] = counts
    return df


# Get all scripts from the webstie
scripts = []
for link in cleaned_strings:
    # Get html, paragraph elements
    html = request_html(link)
    p_tags = html.find_all('p')
    
    # Clear first three p tags (empty)
    p_tags.pop(0)
    p_tags.pop(0)
    p_tags.pop(0)
    
    # Clear last p tags (empty)
    p_tags.pop(-1)
    p_tags.pop(-1)
    p_tags.pop(-1)
    p_tags.pop(-1)
    p_tags.pop(-1)
    
    script = extract_text(p_tags)
    scripts.append(script)
    
    print('*** Script Processed: ' + link)

data_tuples = list(zip(cleaned_strings,scripts))
df = pd.DataFrame(data_tuples, columns=['link', 'scripts'])

count_phrase('Jerry',df)

df.to_csv('Seinfeld_Scripts.csv')

df = pd.read_csv('Seinfeld_Scripts.csv')

df[df.is_that_right != 0]

count_phrase('Sacamano',df)

df