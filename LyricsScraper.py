# A simple script to scrape lyrics from the genius.com based on atrtist name.

import re
import requests

from bs4 import BeautifulSoup
from selenium import webdriver

mybrowser = webdriver.Chrome("E:\chromedriver.exe") # Browser and path to Web driver you wish to automate your tests cases.

user_input = input("Enter Artist Name = ").replace(" ","+") # User_Input = Artist Name
base_url = "https://genius.com/search?q="+user_input # Append User_Input to search query

mybrowser.get(base_url) # Open in browser
file = open('lyrics.txt','a')

while(True): # Reach the bottom of the page.
    mybrowser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = mybrowser.page_source
    soup = BeautifulSoup(html, "lxml")
    time.sleep(3)

pattern = re.compile("[\S]+-lyrics$") # Filter http links that end with "lyrics".
pattern2 = re.compile("\[(.*?)\]") # Remove unnecessary text from the lyrics such as [Intro], [Chorus] etc..


for link in soup.find_all('a',href=True):
        if pattern.match(link['href']):
            f = requests.get(link['href'])
            lyricsoup = BeautifulSoup(f.content,"html.parser")
            lyrics = lyricsoup.find("lyrics").get_text().replace("\n","")
            lyrics = re.sub(pattern2, "", lyrics)
            file.write(lyrics+"\n")
file.close()
