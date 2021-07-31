from tkinter import *
import requests
import json
from PIL import ImageTk, Image
from requests.models import HTTPBasicAuth

class TreeNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class Tree:
    def __init__(self):
        self.size = 0
        self.root = None

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

#Creation of GUI
root = Tk()
root.title('Recades')
root.iconbitmap('images/icon.ico')
root.geometry("900x500")

img = PhotoImage(file='images/launch-background.png')
label = Label(root, image=img).place(x=0, y=0)

field = Entry(root, width=30, justify='center')
field.place(x=357.5, y=400)

#Placing Radio Buttons
var = StringVar()
artist_button = Radiobutton(root, variable=var, value='artist', bg='#FF6A6A', highlightbackground='#000000') 
album_button = Radiobutton(root, variable=var, value='album', bg='#FF6A6A', highlightbackground='#000000')   
track_button = Radiobutton(root, variable=var, value='track', bg='#FF6A6A', highlightbackground='#000000')   
artist_button.place(x=310, y=300)
album_button.place(x=310, y=325)
track_button.place(x=310, y=350)
artist_button.deselect()
album_button.deselect()
track_button.deselect()

#Getting genres
genres = requests.get(BASE_URL + 'recommendations/available-genre-seeds', headers=headers)
genres = genres.json()

def goClick():
    response = str(var.get())
    query = str(field.get())
    
    LIMIT = 5
    search = requests.get(BASE_URL + 'search', headers=headers,
    params={
        'q' : query,
        'type' : response,
        'limit' : LIMIT
    }).json()

    print(search)

    #id = search[response + 's']['items'][0]['id']


go = Button(root, text="GO!", padx=50, pady=50, command=goClick)
go.pack()


root.mainloop()

