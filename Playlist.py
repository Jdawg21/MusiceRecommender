# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import random
from statistics import mode
from statistics import StatisticsError
from scipy.sparse import csr_matrix
import pickle



def personalplaylist(username):
    playlist = []
    pickle_in = open("nn_model.pkl","rb")
    model_nn = pickle.load(pickle_in)
    history = pd.read_csv("datasets/streaminghistory.csv")
    song_df_normalised = pd.read_csv('datasets/song_df_normalised.csv')
    
    
    # in case user is new, then we dont let them access this feature until they serach for a song
    try:
        sentiment_history =history[history['user'] == username]['song_sentiment'].tolist()[0]
        
    except IndexError:
        st.info("please play a few songs before accessing this feature")
    else:
        sentiment_history = sentiment_history.split(",")    
    
    
        try:
            mode(sentiment_history)
        except StatisticsError:
            print('Positive')
            sentiment = 'Positive'
        else:
            print(mode(sentiment_history))
            sentiment =  mode(sentiment_history)
    
    
        if username in history['user'].unique():
            for i in range(history.shape[0]):
                if history.at[i,'user'] == username:
                    song_artist_list = history.at[i,'song_list']
                    song_artist_list = song_artist_list.split(',')
                    
        song_artist_list_freq = []
        for w in song_artist_list:
            song_artist_list_freq.append(song_artist_list.count(w))
            
        song_freq = []
        
        for i in range(len(list(zip(song_artist_list, song_artist_list_freq)))):
            if list(zip(song_artist_list, song_artist_list_freq))[i] not in song_freq:
                song_freq.append(list(zip(song_artist_list, song_artist_list_freq))[i])
        
        song_freq.sort(key = lambda x: x[1], reverse=True)   
        
        song_list = []
        song_artist = []
        
        for i in range(len(song_freq[:3])):
            song_list.append(song_freq[i][0].split("by")[0].strip())
            song_artist.append(song_freq[i][0].split("by")[1].strip())    
            
        
        song_by_artist = [i +" " + j for i, j in zip(song_list, song_artist)]
        
        # recommending similar songs based on songs listened by user
        
        for i in range(len(song_by_artist)):
            #song_df_normalised = song_df_normalised[song_df_normalised['sentiment'] == sentiment]
            
            song_features = song_df_normalised.set_index("song_artist")
            #song_features.drop("Unnamed: 0",axis=1,inplace=True)
            song_features.drop(['track_artist', 'lyrics', 'track_album_name','track_popularity',
                   'playlist_name', 'playlist_genre', 'playlist_subgenre','language','sentiment','track_name','links'],axis=1,inplace=True)
            #song_features.head()
            song_features_csr = csr_matrix(song_features.values)
            #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
            model_nn.fit(song_features_csr)
        
            temp = song_features.copy()
            temp.reset_index(inplace=True)
            songsearch = song_by_artist[i]
            songsearch = songsearch.lower()
            song_index = temp.index[temp['song_artist'] == song_by_artist[i]].tolist()[0]
            #print(song_index)
            #print(song_features.index[song_index])
            distances,indices = model_nn.kneighbors(X = song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=11)
        
            for i in range(1,11):
                if song_features.index[indices.flatten()[i]] not in playlist:
                    playlist.append(song_features.index[indices.flatten()[i]])    
        
        
        
        ## DEALING WITH ARTISTS
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
            
    
        for i in range(len(artist_freq_count[:3])):
            df = song_df_normalised[(song_df_normalised['track_artist'] == artist_freq_count[i][0]) & (song_df_normalised['sentiment'] == sentiment)].sort_values('track_popularity',ascending=False)
            playlist = playlist + df['song_artist'].tolist()[:10]
            
            
        
                
        random.shuffle(playlist)
        for i in range(10):
            c = i + 1
            st.text(str(c)+" : "+playlist[i])
            x = song_df_normalised[(song_df_normalised['song_artist'] == playlist[i])]['links'].tolist()[0]
            components.iframe(src="https://w.soundcloud.com/player/?url="+x+"&color=%23ff5500")
        
        
        
        
def main():
    personalplaylist()
    
        
if __name__  == '__main__':
    main()

        
