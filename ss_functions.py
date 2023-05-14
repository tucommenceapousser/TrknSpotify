#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 10:15:02 2022

@author: halimbouayad
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from requests import *
import pandas as pd
import streamlit as st
import numpy as np
import time

def connect(scope, username):
    scope = "user-library-read"  
    token = SpotifyOAuth(scope=scope, username=username)
    spotifyObject = spotipy.Spotify(auth_manager=token)
    return spotifyObject


def get_features(a):
    
    feature_names = [f for f in a[0]]
    features = []

    for i in range(len(a)):
        
        features.append([a[i][f] for f in a[i]])
#        features=list(np.pad(features, (0, max_length), 'constant'))

    #print(len(features))
    return features, feature_names



def get_artist(liste):
    for i, artists in enumerate(liste):
        if i ==0:
            artist=artists['name']
        else:
            artist=artist+", "+artists['name']
    return artist

@st.cache
def get_data(sp, username):
    playlists = sp.current_user_playlists(limit=50)
   
    tr_names=[]
    pl_urls=[]
    pl_names=[]
    #tracks=[]
    #links=[]
    date_added=[]
    popularity=[]
    ids=[]
    artist_list=[]
    #features=[]
    features=pd.DataFrame()
    df=pd.DataFrame()
    
    while playlists:
        
        
        
        for i, playlist in enumerate(playlists['items']):
            #print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
            # urls.append(playlist['uri'])
            # names.append(playlist['name'])
            # tracks.append(playlist['tracks']['total'])
            # links.append(playlist['external_urls']['spotify'])
            # ids.append(playlist['id'])
            #print(playlist)
            #st.text(last)
            print(playlist)
            playlist_content=sp.playlist(playlist['uri'])
            for i,trax in enumerate(playlist_content['tracks']['items']):
                
                #Track name
                tr_names.append(trax['track']['name'])
                
                #Track ID
                ids.append(trax['track']['id'])
                
                date_added.append(trax['added_at'])
                
                popularity.append(trax['track']['popularity'])
                
                #Playlist Name
                pl_names.append(playlist['name'])
                
                #Track URI
                pl_urls.append(playlist['uri'])
                
                artist_list.append(get_artist(trax['track']['artists']))
                
                test='All done!'
                
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    #audio_analysis


    df['playlist']=pl_names
    df['track']=tr_names
    df['artist']=artist_list
    df['playlist_url']=pl_urls
    df['track_id']=ids
    df['date_added']=date_added
    df['popularity']=popularity
    
    #Audio Features

    # start=0
 
    # for i in range(int(np.ceil(len(df)/50))):
    #     end=max(start+50, len(df))
        
        
        
    #     print('test='+str(i))
    #     print(feat)

    #API only handles batch of 100 of ids
    for start in range(0, len(df), 100):
        
        if start+100>len(df):
            end=len(df)
        else:
            end=start+100
            


        audio_feat=sp.audio_features(df.track_id[start:end])
        
        ##print('audio feat=======')
        #print(audio_feat)
        
        #print('feat=======')
        feat, feat_names = get_features(audio_feat)
        print('-----feat')
        print(feat)
        print('-----features')
        print(features)
        features=pd.concat([features, pd.DataFrame(feat)], axis=0)
        print('-----features')
        print(features)

    #print(len(features))
    
    
    features.columns=feat_names
    
    df=pd.concat([df.reset_index(), features.reset_index()], axis=1)


    
    df=df.drop(columns=['index', 'index'])
    
    #df.to_pickle('./spotify.pkl')
    return df, test

# def playlist_details(sp, df, username):
    
   
    
#     selected=st.selectbox('Please select to zoom', df.name)
#     uri=df[df.name==selected].reset_index()['url'][0]
#     #df_tracks=pd.DataFrame(playlist_content)
    
#     # Connection to Spotipy
#     #sp=connect(scope='user-library_read', username=username)
#     playlist_content=sp.playlist(uri)
#     names=[]
#     releasedays=[]
#     ids=[]
    
#     for i,trax in enumerate(playlist_content['tracks']['items']):
    
#         names.append(trax['track']['name'])
#         #releasedays.append(trax['track']['added_at'])
#         ids.append(trax['track']['id'])
        
#     pl=pd.DataFrame()
#     pl['name']=names
#     #pl['release_date']=releasedays
#     pl['id']=ids
#     st.dataframe(pl)
#     return df 

def EDA(df):
    st.header("EDA")
    #Key Metrics
    f_value=st.selectbox('Select a playlist', df.playlist.unique())
    dff=df[df.playlist==f_value]
    
    cols=['danceability','energy','acousticness','tempo','loudness','valence']
    for col in cols[:2]:
        temp=dff.describe().loc['mean',:][col]
        st.metric(col, '{:.1%}'.format(temp))
    
    st.text('Top songs from that album:')
    st.dataframe(dff)

    selected=st.selectbox('By playlist (click to select other filter)', df.columns)
    st.bar_chart(df[df.playlist==f_value].groupby(selected).agg({'danceability':'mean'}))
 
    
     

    
#if st.button('View playlist!'):
    
# def playlist_overview(sp, username):
#     # scope = "user-library-read"  
#     # token = SpotifyOAuth(scope=scope, username=username)
#     # spotifyObject = spotipy.Spotify(auth_manager=token)
    
    
#     playlists = sp.current_user_playlists(limit=50)
#     print('=================')
#     #response = requests.get("http://localhost:1234", timeout=10)
#     #print(response.json())
#     print('=================')
#     df=pd.DataFrame()   
    
#     urls=[]
#     names=[]
#     tracks=[]
#     links=[]
#     ids=[]
    
#     while playlists:
        
#         for i, playlist in enumerate(playlists['items']):
#             #print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#             urls.append(playlist['uri'])
#             names.append(playlist['name'])
#             tracks.append(playlist['tracks']['total'])
#             links.append(playlist['external_urls']['spotify'])
#             ids.append(playlist['id'])
#             #print(playlist)
#             #st.text(last)
           
      
            
#         if playlists['next']:
#             playlists = sp.next(playlists)
#         else:
#             playlists = None
    
#     #audio_analysis
    
#     df['name']=names
#     df['tracks']=tracks
#     df['url']=urls
#     df['id']=ids
#     st.dataframe(df)   

#[a[0][i] for i in a[0]] 
# 1seFIg83Eac87g1hmtBRjG
# 5ZwRTJD1bTACtIuW5Iibnu