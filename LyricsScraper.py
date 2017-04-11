# A simple script to scrape lyrics from the genius.com based on atrtist name.

import re
import requests
import time
import codecs

from bs4 import BeautifulSoup
from selenium import webdriver

mybrowser = webdriver.Chrome("path\to\chromedriver\binary") # Browser and path to Web driver you wish to automate your tests cases.

user_input = input("Enter Artist Name = ").replace(" ","+") # User_Input = Artist Name
base_url = "https://genius.com/search?q="+user_input # Append User_Input to search query
mybrowser.get(base_url) # Open in browser

t_sec = time.time() + 60*20 # seconds*minutes
while(time.time()<t_sec): # Reach the bottom of the page as per time for now TODO: Better condition to check end of page.
    mybrowser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = mybrowser.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(5)

pattern = re.compile("[\S]+-lyrics$") # Filter http links that end with "lyrics".
pattern2 = re.compile("\[(.*?)\]") # Remove unnecessary text from the lyrics such as [Intro], [Chorus] etc..

with codecs.open('lyrics.txt','a','utf-8-sig') as myfile:
    for link in soup.find_all('a',href=True):
            if pattern.match(link['href']):
                f = requests.get(link['href'])
                lyricsoup = BeautifulSoup(f.content,"html.parser")
                #lyrics = lyricsoup.find("lyrics").get_text().replace("\n","") # Each song in one line.
                lyrics = lyricsoup.find("lyrics").get_text() # Line by Line
                lyrics = re.sub(pattern2, "", lyrics)
                myfile.write(lyrics+"\n")
mybrowser.close()
myfile.close()
