# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from OOPapproach import *
from SongRecommendation import *
import base64
from nltk.sentiment.vader import  SentimentIntensityAnalyzer




def artistsearch():



    userinput = st.text_input("Enter an artist you like ")
    userinput = userinput.lower()
    st.text("your artist is: "+userinput)
    
    
    song_df_normalised = pd.read_csv("datasets/song_df_normalised.csv")
    
    try:
        artist = song_df_normalised[song_df_normalised['track_artist'].str.contains(userinput)]['track_artist'].tolist()[0]
    
    except IndexError:
        st.error("No result :(")
    
    else:
        artist_list = song_df_normalised[song_df_normalised['track_artist'].str.contains(userinput)]['track_artist'].tolist()
        
        artist_list = list(set(artist_list))
        option = st.selectbox("Choose your artist", artist_list)
        x = artist_list.index(option)
        artist_name = artist_list[x]
        
        st.text("Top songs for "+artist_name+" are:")
        
        artist_song_df = song_df_normalised[song_df_normalised['track_artist'] == artist_name]
        artist_song_df = artist_song_df.sort_values('track_popularity',ascending=False)
        artist_song_list = artist_song_df['track_name'].to_list()
        
        
        n = len(artist_song_list)
        if n>10:
            n=10
        for i in range(n):
            c = i + 1
            st.text(str(c)+" : "+artist_song_list[i])    
            
        artist_song_list.clear()
        
        #recommend = st.button("go further ")
        #if recommend:
        #    songrecommender()
   
    
def main():
    artistsearch()
    
        
if __name__  == '__main__':
    main()
