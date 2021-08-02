import pickle
import requests
import json
import random
from requests.models import HTTPBasicAuth

class BTreeNode:
    def __init__(self, leaf=False, degree=0):
        self.leaf = leaf
        self.keys = [[]]*(2*degree-1)
        self.children = [[]]*(2*degree)
        self.number = 0
        self.degree = degree

    def insertNonFull(self, key):
        index = self.number - 1

        if self.leaf == True:
            while index >= 0 and self.keys[index][0] > key[0]:
                self.keys[index+1] = self.keys[index]
                index -= 1
            
            self.keys[index+1] = key
            self.number += 1

        else:
            while index >= 0 and self.keys[index][0] > key[0]:
                index -= 1
            
            if(self.children[index+1].number == 2*self.degree):
                self.spilt(index+1, self.children[index+1])
            
                if self.keys[index+1][0] < key[0]:
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
        while index < self.number and key > self.keys[index][0]:
            index += 1

        if self.keys[index][0] == key:
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
                if node.keys[0][0] < key[0]:
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
        self.adjList = {}
        self.vCount = 0
        self.indexMap = {}

    def insert(self, V1, V2):
        self.adjList[tuple(V1)] = [tuple(V2)]
        self.adjList[tuple(V2)] = [tuple(V1)]
        if tuple(V1) not in self.indexMap:
            self.indexMap[tuple(V1)] = self.vCount
            self.vCount += 1
        if tuple(V2) not in self.indexMap:
            self.indexMap[tuple(V2)] = self.vCount
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

#spotify ids for playlists

#All out 60s
#id: "37i9dQZF1DXaKIA8E7WcJj"

#All out 70s
#id: "37i9dQZF1DWTJ7xPn4vNaz"

#All out 80s
#id: "37i9dQZF1DX4UtSsGT1Sbe"

#All out 90s
#id: "37i9dQZF1DXbTxeAdrVG2l"

#All out 00s
#id: "37i9dQZF1DX4o1oenSJRJd"

#All out 10s
#id: "37i9dQZF1DX5Ejj0EkURtP"

Recades_graph = Graph()
queue = []
query = 'The Beatles'
response = 'artist'

#Gets seed tracks
playlists = {
    0 : "37i9dQZF1DXaKIA8E7WcJj",
    1 : "37i9dQZF1DWTJ7xPn4vNaz",
    2 : "37i9dQZF1DX4UtSsGT1Sbe",
    3 : "37i9dQZF1DXbTxeAdrVG2l",
    4 : "37i9dQZF1DX4o1oenSJRJd",
    5 : "37i9dQZF1DX5Ejj0EkURtP"
}

genre = ['rock', 'pop', 'alternative', 'indie', 'hip hop']
mseed_tracks = [[]]*6
mseed_artists = [[]]*6
for i in range(0, 6):
    playlist = requests.get(BASE_URL + 'playlists/' + playlists[i] + '/tracks',
    headers=headers,
    params={
        'playlist_id' : playlists[i],
        'market' : 'US',
        'fields' : 'items(track(album(artists),id))'
    }).json()
    
    for x in playlist['items']:
        mseed_tracks[i].append(x['track']['id'])
        mseed_artists[i].append(x['track']['album']['artists'][0]['id'])



s_tracks = [[]] * 6
s_artists = [[]] * 6
rec = []
graph_seed = []
#selects random seeds for recommendations
for i in range(6):
    for j in range(5):
        s_tracks[i].append(random.choice(mseed_tracks[i]))
        s_artists[i].append(random.choice(mseed_artists[i]))

    rec.append(requests.get(BASE_URL + 'recommendations', headers=headers,
    params={
        'seed_artist' : s_artists[i],
        'seed_genres' : genre,
        'seed_tracks' : s_tracks[i]
    }).json())

    

    # search = requests.get(BASE_URL + 'search', headers=headers,
    # params={
    #     'q' : query,
    #     'type' : response,
    #     'limit' : LIMIT
    # }).json()

    # id = str(search[response + 's']['items'][0]['id'])


# sixties_tree = BTree(3)
# seventies_tree = BTree()
# eighties_tree = BTree()
# nineties_tree = BTree()
# thousands_tree = BTree()
# tens_tree = BTree()
