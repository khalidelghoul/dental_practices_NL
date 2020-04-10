import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

# Create all urls for each ZorgkaartNederland page with overview of dental practices: scrape_urls
scrape_urls=[]
for i in range(1,2): #substitute second number with number of pages to be scraped
    url='https://www.zorgkaartnederland.nl/tandartsenpraktijk/pagina'+str(i)
    scrape_urls.append(url)

# Use for loops such that for every scrape_url we get the dental practice urls mentioned on the page: praktijken_links
praktijken_links=[]
for url in scrape_urls:
    r=requests.get(url)
    #time.sleep(5)
    soup=BeautifulSoup(r.text, 'html.parser')
    a_tags=soup.find_all('a')
    for link in a_tags:
        website_naam=link.get('href')
        if website_naam is not None:
            if 'zorginstelling' in website_naam:
                if 'waardering' not in website_naam:
                    if 'content' not in website_naam:
                        praktijken_links.append(website_naam)
                        
# Convert to dataframe to drop duplicates and then back to list: praktijken_zorgkaart_websites
df_praktijken_links=pd.DataFrame(praktijken_links)
df_praktijken_links=df_praktijken_links.drop_duplicates()
praktijken_zorgkaart_websites=df_praktijken_links.iloc[:,0].tolist()

# Get address information for each practice and save in list of lists with four elements in each sublist: city, practice name, postal code, and address: praktijk_info
praktijk_info=[]
for url in praktijken_zorgkaart_websites:
    url="https://www.zorgkaartnederland.nl"+url
    r=requests.get(url)
    soup=BeautifulSoup(r.text, 'html.parser')
    span_tags=soup.find_all('meta')
    praktijken_addressen=[]
    praktijk_locatie_gegevens=[]
    for span in span_tags:
        address=span.get('content')
        praktijken_addressen.append(address)
        praktijk_locatie_gegevens.append(praktijken_addressen[8:13])
    praktijk_info.append(praktijk_locatie_gegevens[13])

# Convert list of lists to dataframe: df_praktijken
df_praktijken=pd.DataFrame.from_records(praktijk_info, columns=['Straat', 'Postcode', 'Stad', 'Summary', 'Naam'])
