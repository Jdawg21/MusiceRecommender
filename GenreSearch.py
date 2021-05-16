# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from OOPapproach import *
from SongRecommendation import *
import base64
from nltk.sentiment.vader import  SentimentIntensityAnalyzer




def genresearch():

    
    
    song_df_normalised = pd.read_csv("datasets/song_df_normalised.csv")
    
    #genre_list = song_df_normalised[song_df_normalised['playlist_subgenre'].str.contains(userinput)]['playlist_subgenre'].tolist()
    #genre_list = list(set(genre_list))
    
    genre_list = song_df_normalised['playlist_subgenre'].unique().tolist()
    
    option = st.selectbox("Choose your Genre", genre_list)
    x = genre_list.index(option)
    genre_name = genre_list[x]
    
    st.text("Top songs for "+genre_name+" are:")
    
    genre_song_df = song_df_normalised[song_df_normalised['playlist_subgenre'] == genre_name]
    genre_song_df =  genre_song_df.sort_values('track_popularity',ascending=False)
    genre_list =  genre_song_df['track_name'].to_list()
    genre_artist_list =  genre_song_df['track_artist'].to_list()
    
    genre_song_list=[i +" by " + j for i, j in zip(genre_list, genre_artist_list)]
    
    n = len(genre_song_list)
    if n>10:
        n=10
    for i in range(n):
        c = i + 1
        st.text(str(c)+" : "+ genre_song_list[i])    
        
    genre_song_list.clear()
    
    #recommend = st.button("go further ")
    #if recommend:
    #    songrecommender()
   
    
def main():
    genresearch()
    
        
if __name__  == '__main__':
    main()
