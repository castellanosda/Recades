from tkinter import *
from PIL import ImageTk, Image
import requests
import json
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
    def insert(self, node, integer):
        if self.root == None:
            self.root = TreeNode(integer)
            return
        if node == None:
            node = TreeNode(integer)
            return node
        elif node.data < integer:
            node.right = self.insert(node.right, integer)
        elif node.data > integer:
            node.left = self.insert(node.left, integer)
        elif node.data == integer:
            return
        
        return node

    def inorder(self, node):
        if node != None:
            if node.left != None:
                self.inorder(node.left)
            print(node.data)
            if node.right != None:
                self.inorder(node.right)

class Graph:
    def __init__(self):
        self.adjList = {}
        self.vCount = 0
        self.indexMap = {}

    def insert(self, V1, V2):
        self.adjList[V1].append(V2)
        self.adjList[V2].append(V1)
        if V1 not in self.indexMap:
            self.indexMap[V1] = self.vCount
            self.vCount += 1
        if V2 not in self.indexMap:
            self.indexMap[V2] = self.vCount
            self.vCount += 1
        
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

#Getting genres
genres = requests.get(BASE_URL + 'recommendations/available-genre-seeds', headers=headers)
genres = genres.json()

def goClick():
    response = str(var.get())
    query = str(field.get())
    
    LIMIT = 1
    search = requests.get(BASE_URL + 'search', headers=headers,
    params={
        'q' : query,
        'type' : response,
        'limit' : LIMIT
    }).json()

    id = str(search[response + 's']['items'][0]['id'])

    id_json = requests.get(BASE_URL + response + 's/' + id, headers=headers,
    params={
        'id' : id,
    }).json()

    print(id_json['genres'])


go = Button(root, text="GO!", padx=50, pady=3, command=goClick)
go.place(x=370, y=427)


root.mainloop()

