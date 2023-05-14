#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 10:48:49 2022

@author: halimbouayad
"""

import pandas as pd
import numpy as np


from datetime import datetime 
import os

# #load data

# dir = os.getcwd()
# path = os.path.join(dir, 'data.csv')

# try:
#     df=pd.read_csv(path)
#     df_continent=pd.DataFrame(df.groupby('continent').total_deaths.sum())
# except:
#     print('Error has occured')


    
    
# ################################################

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from requests import *
import pandas as pd
import streamlit as st


# Custom imports
import ss_functions 
from ss_functions import *
import env_variables
username = "hyder14"






st.title('Spotify Playlist Shuffler')

st.text('The goal of this project is to gain better control of your playlists\n while exploring the features of the Spotify Web API.')


    
with st.expander('Create a playlist'):


    st.header('Create a playlist')
    st.write('Hello, *World!* :sunglasses:')
    
    scope = "playlist-modify-public"


    token = util.prompt_for_user_token(username,scope,client_id=os.environ['SPOTIPY_CLIENT_ID'],client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])
    spotifyObject = spotipy.Spotify(auth=token)

    
    #create the playlist
    playlist_name = st.text_input('Enter a playlist name = ')
    playlist_description = st.text_input('Enter a playlist description = ')

    if st.button('Create playlist!'):
        token = util.prompt_for_user_token(username,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)
        spotifyObject = spotipy.Spotify(auth=token)
        spotifyObject.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)



with st.expander('List of current playlists'):
    
    st.header("List of playlist")
    
    sp=connect(scope='user-library_read', username=username)
    
    df, test=get_data(sp, username)
    st.dataframe(df)
    
    st.text(test)
    
    
with st.expander('What do your playlists look like?'):
    if isinstance(df, pd.DataFrame):
        EDA(df)
        
        
      
