# -*- coding: utf-8 -*-
"""
Created on Tue May  4 21:15:40 2021

@author: Jos.
"""

import streamlit as st
import pandas as pd
from OOPapproach import *
import base64
from nltk.sentiment.vader import  SentimentIntensityAnalyzer


def songrecommender(username):

    mood = st.text_input("How are you today "+str(username)+"?")
    
    score = SentimentIntensityAnalyzer().polarity_scores(mood)
    if score['compound'] >= 0.05:
            st.success('Positive Sentiment Detected')
            sentiment = 'Positive'
    elif score['compound'] > -0.05 and score['compound'] < 0.05:
            st.info('Neutral Sentiment Detected')
            sentiment = 'Neutral'
    elif score['compound'] <= -0.05:
            st.error('Negative Sentiment Detected')
            sentiment = 'Negative'    



    
    userinput = st.text_input("Enter a song you would like to get recommendations for: ")
    userinput = userinput.lower()
    st.text("your song is: "+userinput)
    
    
    song_df_normalised = pd.read_csv("datasets/song_df_normalised.csv")
    
    try:
        song_name =song_df_normalised[song_df_normalised['track_name'].str.contains(userinput)]['track_name'].tolist()[0]
        #song_name = st.selectbox("choose your song", song_dataset)
    
    except IndexError:
        #print("Sorry!! We couldnt get any results for", userinput, " :( ")
        string = "Sorry!! We couldnt get any results for "+ str(userinput) +" :("
        st.error(string)
        result = 'fail'
        accurate= 'no'
        user_review(username, userinput,result,accurate)
        
    
    else:
        result='success'
        song_artist_list =[]
        artist_list = []
        song_name_list =song_df_normalised[song_df_normalised['track_name'].str.contains(userinput)]['track_name'].tolist()
        artist_list = song_df_normalised[song_df_normalised['track_name'].str.contains(userinput)]['track_artist'].tolist()
        
        #for i in range(len(song_name_list)):
        #    song_artist_list.append(song_name_list[i]+" by "+artist_list[i])
        
        song_artist_list=[i +" by " + j for i, j in zip(song_name_list, artist_list)]
        
        option = st.selectbox("choose your song", song_artist_list)
        x = song_artist_list.index(option)
        song_name = song_name_list[x]
        
        st.text("song from dataset: "+song_name)
        artist_name = artist_list[x]
        #artist_name = song_df_normalised[song_df_normalised['track_name'] == song_name]['track_artist'].tolist()[0]
        st.text("artist name:"+artist_name)    
        
        genre = song_df_normalised[song_df_normalised['track_name'] == song_name]['playlist_genre'].tolist()[0]
        #st.text("genre of song:"+genre)
        
        subgenre = song_df_normalised[song_df_normalised['track_name'] == song_name]['playlist_subgenre'].tolist()[0]
        #st.text("subgenre of song:"+subgenre)
        
        
        recommend = st.button("click for receommendations ")
        if recommend:
            getartistsongs(artist_name,song_name)
            
            
            getsongsgenre(genre,song_name)
            getsongsubgenre(subgenre,song_name)
        
            getsimilarsongs(song_name)
            output = display()
            #outputlist = list(set(output))
            
            artist_list2 =[]
            for i in range(len(output)):
                artist_list2.append(song_df_normalised[song_df_normalised['track_name'] == output[i]]['track_artist'].tolist()[0])
            
            song_artist_output=[i +" by " + j for i, j in zip(output, artist_list2)]
            
            sentiment_list =[]
            popularity_list =[]
            
            
            for i in range(len(output)):
                sentiment_list.append(song_df_normalised[(song_df_normalised['track_name'] == output[i]) & (song_df_normalised['track_artist'] == artist_list2[i])]['sentiment'].tolist()[0])
                popularity_list.append(song_df_normalised[(song_df_normalised['track_name'] == output[i]) & (song_df_normalised['track_artist'] == artist_list2[i])]['track_popularity'].tolist()[0])
            
            
            
            d = {'songs': song_artist_output,'sentiment': sentiment_list,'popularity':popularity_list}
            song_sentiment = pd.DataFrame(data=d)
            
            
            if sentiment == 'Positive':
                song_sentiment.sort_values(by=['sentiment','popularity'],ascending=[False,False],inplace=True)
            if sentiment == 'Negative':
                song_sentiment.sort_values(by=['sentiment','popularity'],ascending=[True,False],inplace=True)
            
            #if len(song_artist_output) > 10:
            #    n = 10
            #else:
            song_artist_output = song_sentiment['songs'].tolist()
            n = len(song_artist_output)
                
            for i in range(n):
                c = i + 1
                st.text(str(c)+" : "+song_artist_output[i])
        
            clearlist()
        
        #songsearch = userinput
        accurate = st.radio("Were the recommendations accurate?",['yes','no'])
        if accurate == "yes":
            st.success("Awesome")
        if accurate == 'no':
            st.error("Oh no!! We're sorry to hear that")
            
        thankyou = st.button("THANK YOU!!")
        if thankyou:
            final = user_review(username, userinput,result,accurate)
            st.text(final)
     

def main():
    songrecommender()

        
if __name__  == '__main__':
    main()

