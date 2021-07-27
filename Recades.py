from tkinter import *
import requests
import json
from requests.models import HTTPBasicAuth

#Authentification for Spotify API
CLIENT_ID = '6a7ad589234b45b2b9d53799c60562d8'
CLIENT_SECRET = '76823465d7e24630815c65229ad276fa'
AUTH_URL = 'https://accounts.spotify.com/api/token'

#POST
auth_response = requests.post(AUTH_URL, {
    'grant_type' : 'client_credentials',
    'client_id' : CLIENT_ID,
    'client_secret' : CLIENT_SECRET,
})

#Converting response to json
auth_response_data = auth_response.json()

#Saving the access token
access_token = auth_response_data['access_token']

#Header for GET
headers = {
    'Authorization' : 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'

#Getting genres
genres = requests.get(BASE_URL + 'recommendations/available-genre-seeds', headers=headers)
genres = genres.json()

#Ask for artist or album
print('Enter either "track", "album", or "artist"')
response = ''
while True:
    response = input()
    if(response == 'artist' or response == 'album' or response == 'track'):
        break
    else:
        print('Please enter a valid input')

#get ID for track or abum
if(response == 'track'):
    print('Enter a ' + response)
else:
    print('Enter an ' + response)

query = input()

LIMIT = 5
search = requests.get(BASE_URL + 'search', headers=headers,
    params={
        'q' : query,
        'type' : response,
        'limit' : LIMIT
    }).json()

index = 0
while index < LIMIT:
    id = search['artists']['items'][index]['id']
    print("Result: " + search['artists']['items'][index]['name'])
    print("Is this correct? y/n")
    inp = input()
    if inp == 'y':
        break
    else:
        index = index + 1