from tkinter import *
from PIL import ImageTk, Image
import pickle
import requests
import json
from requests.models import HTTPBasicAuth
from collections import deque, defaultdict

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

class BTreeNode:
    def __init__(self, leaf=False, degree=0):
        self.leaf = leaf
        self.keys = [[(), []]]*(2*degree-1)
        self.children = [[]]*(2*degree)
        self.number = 0
        self.degree = degree

    def insertNonFull(self, key):
        index = self.number - 1

        if self.leaf == True:
            while index >= 0 and self.keys[index][0][0] > key[0][0]:
                self.keys[index+1] = self.keys[index]
                index -= 1
            
            self.keys[index+1] = key
            self.number += 1

        else:
            while index >= 0 and self.keys[index][0][0] > key[0][0]:
                index -= 1
            
            if(self.children[index+1].number == 2*self.degree):
                self.spilt(index+1, self.children[index+1])
            
                if self.keys[index+1][0][0] < key[0][0]:
                    index += 1
            
            self.children[index+1].insertNonFull(key)



    def split(self, index, c):

        key_storage = BTreeNode(c.leaf, c.degree)
        key_storage.number = c.degree - 1

        for i in range(self.degree - 1):
            key_storage.keys[i] = c.keys[i+self.degree]

        #copying the last 'degree' children of c to key_storage
        if c.leaf == False:
            for i in range(0, self.degree):
                key_storage.children[i] = c.children[i+self.degree]
        
        #cutting down the number of keys in c
        c.number = self.degree - 1

        #self is going to receive new child
        #space will be made
        for i in range(self.number, index, -1):
            self.children[i+1] = self.children[i]
        
        #linking new child to self
        self.children[index+1] = key_storage

        #moving c keys to self and rearranging
        for i in range(self.number, index - 1, -1):
            self.keys[i+1] = self.keys[i]
        
        #middle key of c will go to this node
        self.keys[index] = c.keys[self.degree - 1]

        #Increment key count of self
        self.number += 1

    def search(self, key):
        index = 0
        while index < self.number and key > self.keys[index][0][0]:
            index += 1

        if self.keys[index][0][0] == key:
            return self

        if self.leaf == True:
            return None

        return self.children[index].search(key)


class BTree:
    def __init__(self, minDegree):
        self.root = None
        self.minDegree = minDegree


    def insert(self, key):
        if self.root == None:
            self.root = BTreeNode(True, self.minDegree)
            self.root.keys[0] = key
            self.root.number += 1
        else:
            #this is so fun!
            if self.root.number == 2*self.minDegree - 1:
                #making a new root
                node = BTreeNode(False, self.minDegree)

                #old root is child of new root
                node.children[0] = self.root

                #split old root
                node.split(0, self.root)

                index = 0
                if node.keys[0][0][0] < key[0][0]:
                    index += 1
                node.children[index].insertNonFull(key)

                self.root = node
            else:
                self.root.insertNonFull(key)
                


    def search(self, key):
        return None if (self.root == None) else self.root.search(key)

#The benefit of graphs is that I will build the graph
#by simply using recursive calls of the spotify recommended artists
#and making the recommendations based off of adjacency
class Graph:
    def __init__(self):
        self.adjList = defaultdict(list)
        self.vCount = 0
        self.indexMap = {}
        self.firstInserts = []

    def insert(self, V1, V2):
        if V1 != V2 and V2 not in self.adjList[tuple(V1)] and V1 not in self.adjList[tuple(V2)]:
            self.adjList[tuple(V1)].append(tuple(V2))
            self.adjList[tuple(V2)].append(tuple(V1))
        if tuple(V1) not in self.indexMap:
            self.indexMap[tuple(V1)] = self.vCount
            self.vCount += 1
        if tuple(V2) not in self.indexMap:
            self.indexMap[tuple(V2)] = self.vCount
            self.vCount += 1
    
    def Display_AdjList(self):
        for item in self.adjList.items():
            print(item)
    def Display_Indices(self):
        for item in self.indexMap.items():
            print(item)
    
    def BFS(self, name, id, decade):
        visited = set()
        queue = deque()
        found = []
        artist = (name, id)
        queue.append(artist)
        while queue:
            current = queue.pop()

            if current != artist:
                #Getting the top track of the artist
                top_track = requests.get(BASE_URL + 'artists/' + current[1] + '/top-tracks',
                headers=headers,
                params={
                    'id' : current[1],
                    'market' : 'US'
                }).json()

                #Checking release data
                release_data_req = requests.get(BASE_URL + 'albums/' + top_track['tracks'][0]['album']['id'],
                headers=headers,
                params={
                    'id' : top_track['tracks'][0]['album']['id']
                }).json()

                release_date = release_data_req['release_date']
                release_date = release_date[:4]
                data = int(release_date) % 100 // 10

                if data == decade:
                    found.append(current[0])
                if len(found) == 5:
                    print(found)
                    return found

            for neighbor in self.adjList[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

#Load data
picklefile = open('RecadesGraph.p', 'rb')

Recades_graph = pickle.load(picklefile)

picklefile.close()

print(Recades_graph.adjList[(('The Beatles'),('3WrFJ7ztbogyGnTHbHJFl2'))])


#Creation of GUI
root = Tk()
root.title('Recades')
root.iconbitmap('images/icon.ico')
root.geometry("900x500")


#loading images
img = PhotoImage(file='images/launch-background.png')
img2 = PhotoImage(file='images/blank.png')
img60 = PhotoImage(file='images/sixties.png')
img70 = PhotoImage(file='images/seventies.png')
img80 = PhotoImage(file='images/eighties.png')
img90 = PhotoImage(file='images/nineties.png')
img00 = PhotoImage(file='images/thousands.png')
img10 = PhotoImage(file='images/tens.png')
label = Label(root, image=img)
label.grid(row=0, column=0)

field = Entry(root, width=30, justify='center')
field.place(x=362.5, y = 400)


#Placing Radio Buttons
var = StringVar()
artist_button = Radiobutton(root, variable=var, value='artist', bg='#CDC2DF', highlightbackground='#CDC2DF')
artist_button.place(x=290, y=303) 
album_button = Radiobutton(root, variable=var, value='album', bg='#CDC2DF', highlightbackground='#CDC2DF') 
album_button.place(x=290, y = 335) 
track_button = Radiobutton(root, variable=var, value='track', bg='#CDC2DF', highlightbackground='#CDC2DF')
track_button.place(x=290, y=366)

artist_name = str()
artist_id = str()

#Decade button function
def sixtiesClick():
    reckies = Recades_graph.BFS(artist_name, artist_id, 6)

    global label
    label.grid_forget()

    label.configure(image=img60)
    label.grid(row=0, column=0)

    artist_text = str()
    for x in reckies:
        artist_text += x + '\n'

    text = Label(root, text=artist_text)
    text.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)

def seventiesClick():
    reckies = Recades_graph.BFS(artist_name, artist_id, 7)

    global label
    label.grid_forget()

    label.configure(image=img70)
    label.grid(row=0, column=0)

    artist_text = str()
    for x in reckies:
        artist_text += x + '\n'

    text = Label(root, text=artist_text)
    text.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)

def eightiesClick():
    reckies = Recades_graph.BFS(artist_name, artist_id, 8)

    global label
    label.grid_forget()

    label.configure(image=img80)
    label.grid(row=0, column=0)

    artist_text = str()
    for x in reckies:
        artist_text += x + '\n'

    text = Label(root, text=artist_text)
    text.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)
    
def ninetiesClick():
    reckies = Recades_graph.BFS(artist_name, artist_id, 9)

    global label
    label.grid_forget()

    label.configure(image=img90)
    label.grid(row=0, column=0)

    artist_text = str()
    for x in reckies:
        artist_text += x + '\n'

    text = Label(root, text=artist_text)
    text.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)

def thousandsClick():
    reckies = Recades_graph.BFS(artist_name, artist_id, 0)

    global label
    label.grid_forget()

    label.configure(image=img00)
    label.grid(row=0, column=0)

    artist_text = str()
    for x in reckies:
        artist_text += x + '\n'

    text = Label(root, text=artist_text)
    text.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)

def tensClick():
    reckies = Recades_graph.BFS(artist_name, artist_id, 1)

    global label
    label.grid_forget()

    label.configure(image=img10)
    label.grid(row=0, column=0)

    artist_text = str()
    for x in reckies:
        artist_text += x + '\n'

    text = Label(root, text=artist_text)
    text.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)

#decade buttons
sixtiesbutton = Button(root, text='60s', padx=39, pady=36, command=sixtiesClick)
seventiesbutton = Button(root, text='70s', padx=39, pady=36, command=seventiesClick)
eightiesbutton = Button(root, text='80s', padx=39, pady=36, command=eightiesClick)
ninetiesbutton = Button(root, text='90s', padx=39, pady=36, command=ninetiesClick)
thousandsbutton = Button(root, text='00s', padx=39, pady=36, command=thousandsClick)
tensbutton = Button(root, text='10s', padx=39, pady=36, command=tensClick)


def goClick():
    #retrieves the id for the 
    response = str(var.get())
    query = str(field.get())

    search = requests.get(BASE_URL + 'search',
    headers=headers,
    params={
        'query' : query,
        'type' : response,
        'limit' : 1
    }).json()

    print(search)
    global artist_name
    global artist_id

    artist_name = search['artists']['items'][0]['name']
    artist_id = search['artists']['items'][0]['id']

    print(artist_name)
    print(artist_id)


    global label

    label.grid_forget()
    field.place_forget()
    artist_button.place_forget()
    album_button.place_forget()
    track_button.place_forget()
    go.place_forget()

    label.config(image=img2)
    label.grid(row=0, column=0)

    sixtiesbutton.place(x=145, y=400)
    seventiesbutton.place(x=250, y=400)
    eightiesbutton.place(x=355, y=400)
    ninetiesbutton.place(x=460, y=400)
    thousandsbutton.place(x=565, y=400)
    tensbutton.place(x=670, y=400)

    
    
go = Button(root, text="GO!", padx=20, pady=20, command=goClick)
go.place(x=417.5, y=423)


root.mainloop()

