from selenium import webdriver
import os 
import requests 
import bs4
import pandas as pd
import numpy as np

#pip install selenium
# download chrome driver: https://chromedriver.chromium.org/
track_url = "https://soundcloud.com/search/sounds?q="

browser = webdriver.Chrome("path to webdriver")
browser.get("https://soundcloud.com")
song_df_normalised =  pd.read_csv("datasets/song_df_normalised.csv")

for i in range(song_df_normalised.shape[0] ):
    x = song_df_normalised['track_name'][i].split('-')[0].strip()
    name = x +" "+ song_df_normalised['track_artist'][i]
    #start_time = time.time()

    "%20".join(name.split(" "))
    browser.get(track_url + name)

    url = "https://soundcloud.com/search/sounds?q=" + name
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text,"html.parser")
    tracks = soup.select("h2")[:]
    track_links = []
    track_names = []

    for index, track in enumerate(tracks):
        track_links.append(track.a.get("href"))
        track_names.append(track.text)
        #print(str(index+1) + ": " + track.text)
        break

    if len(track_links) == 0:
        song_df_normalised.at[i,'links'] = "no link available"
    
    else:
        #browser.get("http://soundcloud.com" + track_links[0])
        print(i,":","http://soundcloud.com" + track_links[0])
        #print(i)
        song_df_normalised.at[i,'links'] = "http://soundcloud.com" + track_links[0]
