# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import random
from statistics import mode
from statistics import StatisticsError


def personalplaylist(username):
    history = pd.read_csv("datasets/streaminghistory.csv")
    song_df_normalised = pd.read_csv('datasets/song_df_normalised.csv')

    if username in history['user'].unique():
        for i in range(history.shape[0]):
            if history.at[i,'user'] == username:
                song_artist_list = history.at[i,'song_list']
                song_artist_list = song_artist_list.split(',')
                
    
    
    
    
    artist_list = []
    artist_freq = []
    
    for i in range(len(song_artist_list)):
        artist_list.append(song_artist_list[i].split('by')[1].strip())
        
    for w in artist_list:
        artist_freq.append(artist_list.count(w))
                    
    artist_freq_count = []
    
    for i in range(len(list(zip(artist_list, artist_freq)))):
        if list(zip(artist_list, artist_freq))[i] not in artist_freq_count:
            artist_freq_count.append(list(zip(artist_list, artist_freq))[i])  

    artist_freq_count.sort(key = lambda x: x[1], reverse=True)    

    sentiment_history =history[history['user'] == username]['song_sentiment'].tolist()[0]
    sentiment_history = sentiment_history.split(",")
    
    try:
        mode(sentiment_history)
    except StatisticsError:
        print('Positive')
        sentiment = 'Positive'
    else:
        print(mode(sentiment_history))
        sentiment =  mode(sentiment_history)
              
        
    playlist = []
    for i in range(len(artist_freq_count[:3])):
        df = song_df_normalised[(song_df_normalised['track_artist'] == artist_freq_count[i][0]) & (song_df_normalised['sentiment'] == sentiment)].sort_values('track_popularity',ascending=False)
        playlist = playlist + df['song_artist'].tolist()[:4]
            
    random.shuffle(playlist)
    n = len(playlist)
    if n>10:
        n=10
    for i in range(n):
        c = i + 1
        st.text(str(c)+" : "+playlist[i])
        x = song_df_normalised[(song_df_normalised['song_artist'] == playlist[i])]['links'].tolist()[0]
        components.iframe(src="https://w.soundcloud.com/player/?url="+x+"&color=%23ff5500")
        
        
        
        
def main():
    personalplaylist()
    
        
if __name__  == '__main__':
    main()

        