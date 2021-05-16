# -*- coding: utf-8 -*-

import nltk
from nltk.sentiment.vader import  SentimentIntensityAnalyzer
import streamlit as st
import pandas as pd
import base64
from SongRecommendation import *
from ArtistSearch import *
from GenreSearch import *


def main():
    intro = " Hi! I'm MARC, short for Music Analysis and Recommender Chatbot \n (well, my devs are still working on the chatbot, so you can call me MAR)\n Would you mind spending a few minutes to test me out?"
    st.text(intro)
    username = st.text_input("Whats your name?")
    
    if username == 'devtesterMARCauthenticcationPaSSworDLJJR':
        st.info("Suppp")
        df = pd.read_csv("datasets/user-review.csv")
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="user-review.csv">Download CSV File</a>'
            return href
        
        st.markdown(filedownload(df), unsafe_allow_html=True)
        
    else:
        st.text("Nice to meet you "+str(username))
    
#   mood = st.text_input("How are you today "+str(name)+"?")
#    score = SentimentIntensityAnalyzer().polarity_scores(mood)
#    if score['compound'] >= 0.05:
#            st.success('Positive Sentiment Detected')
#            sentiment = 'Positive'
#    elif score['compound'] > -0.05 and score['compound'] < 0.05:
#            st.info('Neutral Sentiment Detected')
#            sentiment = 'Neutral'
#    elif score['compound'] <= -0.05:
#            st.error('Negative Sentiment Detected')
#            sentiment = 'Negative'
  
    
  
    option = st.selectbox("What would you like to do?", 
                          ['Search Artist','Get song reccomendations','Browse by genre'])
    st.text(option)
    #gorecommend = st.button("go: ")
    #if gorecommend:
    if option == 'Get song reccomendations':
        songrecommender(username)
    if option == 'Search Artist':
        artistsearch()        
     
    if option == 'Browse by genre':
        genresearch()
    
  
    
if __name__  == '__main__':
    main()


