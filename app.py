# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
#from OOPapproach import *
import base64
from scipy.sparse import csr_matrix
import pickle

song_df_normalised = pd.read_csv("datasets/song_df_normalised.csv")
song_df_normalised.head()

pickle_in = open("nn_model.pkl","rb")
model_nn = pickle.load(pickle_in)

global recommended_song_list
recommended_song_list =[]

def getsimilarsongs(song_name):
    
    song_features = song_df_normalised.set_index("track_name")
    #song_features.drop("Unnamed: 0",axis=1,inplace=True)
    song_features.drop(['track_artist', 'lyrics', 'track_album_name',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language'],axis=1,inplace=True)
    #song_features.head()
    song_features_csr = csr_matrix(song_features.values)
    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(song_features_csr)

    temp = song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)
    #print(song_features.index[song_index])
    distances,indices = model_nn.kneighbors(X = song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)

    for i in range(1,5):
        if song_features.index[indices.flatten()[i]] not in recommended_song_list:
            recommended_song_list.append(song_features.index[indices.flatten()[i]])


def getartistsongs(artist_name,song_name):
    artist_data = song_df_normalised[song_df_normalised['track_artist'] == artist_name]
    artist_song_features=artist_data.set_index("track_name")
    artist_song_features.drop(['track_artist', 'lyrics', 'track_album_name',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language'],axis=1,inplace=True)
    #artist_song_features.head()
    #from scipy.sparse import csr_matrix

    artist_song_features_csr = csr_matrix(artist_song_features.values)

    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(artist_song_features_csr)

    temp = artist_song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)

    #print(artist_song_features.index[song_index])

    if artist_data.shape[0] < 6:
        n = artist_data.shape[0]
        distances,indices = model_nn.kneighbors(X = artist_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=n)
        for i in range(1,n): 
            recommended_song_list.append(artist_song_features.index[indices.flatten()[i]])
    else:    
        distances,indices = model_nn.kneighbors(X = artist_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)
        for i in range(1,5): 
            if artist_song_features.index[indices.flatten()[i]] not in  recommended_song_list:
                recommended_song_list.append(artist_song_features.index[indices.flatten()[i]])

 

def getsongsgenre(genre,song_name):
    genre_data = song_df_normalised[song_df_normalised['playlist_genre'] == genre]
    genre_song_features=genre_data.set_index("track_name")
    genre_song_features.drop(['track_artist', 'lyrics', 'track_album_name',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language'],axis=1,inplace=True)
    #genre_song_features.head()
    #from scipy.sparse import csr_matrix

    genre_song_features_csr = csr_matrix(genre_song_features.values)

    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(genre_song_features_csr)

    temp = genre_song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)

    #print(genre_song_features.index[song_index])


    distances,indices = model_nn.kneighbors(X = genre_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)

    for i in range(1,5): 
        if genre_song_features.index[indices.flatten()[i]] not in recommended_song_list:
            recommended_song_list.append(genre_song_features.index[indices.flatten()[i]])
        

def getsongsubgenre(subgenre,song_name):
    subgenre_data = song_df_normalised[song_df_normalised['playlist_subgenre'] == subgenre]
    subgenre_song_features=subgenre_data.set_index("track_name")
    subgenre_song_features.drop(['track_artist', 'lyrics', 'track_album_name',
           'playlist_name', 'playlist_genre', 'playlist_subgenre','language'],axis=1,inplace=True)
    #subgenre_song_features.head()
    #from scipy.sparse import csr_matrix

    subgenre_song_features_csr = csr_matrix(subgenre_song_features.values)

    #model_nn = NearestNeighbors(metric='cosine',algorithm='brute')
    model_nn.fit(subgenre_song_features_csr)

    temp = subgenre_song_features.copy()
    temp.reset_index(inplace=True)
    songsearch = song_name
    songsearch = songsearch.lower()
    song_index = temp.index[temp['track_name'] ==songsearch].tolist()[0]
    #print(song_index)

    #print(subgenre_song_features.index[song_index])


    distances,indices = model_nn.kneighbors(X = subgenre_song_features.iloc[song_index,:].values.reshape(1,-1), n_neighbors=6)      

    for i in range(1,5): 
        if subgenre_song_features.index[indices.flatten()[i]] not in recommended_song_list:
            recommended_song_list.append(subgenre_song_features.index[indices.flatten()[i]])
        
        
        

def display():
    return  recommended_song_list


def clearlist():
    recommended_song_list.clear()


def user_review(username, songsearch,result,accurate):
    import pandas as pd
    #print(username, songsearch,result,accurate)
    df = pd.read_csv("datasets/user-review.csv")
    id = df.shape[0] + 1
    df2 = pd.DataFrame({'id':[id],'user_name':[username], 'song_searched':[songsearch], 
                        'result':[result],'accurate':[accurate]})
    df = df.append(df2,ignore_index=True)
    df.to_csv("datasets/user-review.csv",index=False)
    text = "You're cool!!"
    return text


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
            if len(output) > 10:
                n = 10
            else:
                n = len(output)
                
            for i in range(n):
                c = i + 1
                st.text(str(c)+" : "+output[i])
        
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
     
        
if __name__  == '__main__':
    main()

