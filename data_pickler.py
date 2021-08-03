import pickle
import requests
import json
import random
from requests.models import HTTPBasicAuth
from collections import deque, defaultdict

class BTreeNode:
    def __init__(self, leaf=False, degree=0):
        self.leaf = leaf
        self.keys = [[(), []]]*(2*degree)
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
                self.split(index+1, self.children[index+1])
            
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
            print('hello' + str(self.root.number))
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
    
    def BFS(self):
        visited = set()
        queue = deque()
        for x in self.firstInserts:
            visited.add(x)
            queue.append(x)
        
        while queue:
            current = queue.pop(0)
            print(current, end = " ")

            for neighbor in self.adjList[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    

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


#Recades_graph = Graph()  <--Ran this once to create the object that will be pickled
queue = []
query = 'The Beatles'
response = 'artist'

#Gets seed tracks and artists from featured All out ##s playlists
playlists = {
    0 : "37i9dQZF1DXaKIA8E7WcJj",
    1 : "37i9dQZF1DWTJ7xPn4vNaz",
    2 : "37i9dQZF1DX4UtSsGT1Sbe",
    3 : "37i9dQZF1DXbTxeAdrVG2l",
    4 : "37i9dQZF1DX4o1oenSJRJd",
    5 : "37i9dQZF1DX5Ejj0EkURtP"
}

mseed_tracks = []
mseed_artists = []
for i in range(6):
    mseed_artists.append([])
    mseed_tracks.append([])
    

for i in range(6):
    playlist = requests.get(BASE_URL + 'playlists/' + playlists[i] + '/tracks',
    headers=headers,
    params={
        'playlist_id' : playlists[i],
        'market' : 'US',
        'fields' : 'items(track(album(artists),id))'
    }).json()
    
    for x in playlist['items']:
        mseed_tracks[i].append(x['track']['id'])
        mseed_artists[i].append(x['track']['album']['artists'][0]['name'])

s_tracks = [[]]
s_artists = [[]]
for i in range(6):
    s_tracks.append([])
    s_artists.append([])
rec = []
graph_seed = []

rec_queue = deque()


#Data perserverance using python's pickling
picklefile = open('RecadesGraph.p', 'rb')

Recades_graph = pickle.load(picklefile)

picklefile.close()


#selects random seeds for recommendations
# for i in range(6):
#     for j in range(5):
#         randtrack = random.choice(mseed_tracks[i])
#         randartist = random.choice(mseed_artists[i])
#         s_tracks[i].append(randtrack)
#         s_artists[i].append(randartist)

#     #uses random seed to generate beginnings of graph
#     rec.append(requests.get(BASE_URL + 'recommendations', headers=headers,
#     params={
#         'seed_artist' : s_artists[i],
#         'seed_tracks' : s_tracks[i]
#     }).json())

#     #adding first recs to the rec queue!
#     rec_queue.append((rec[i]['tracks'][0]['artists'][0]['name'], rec[i]['tracks'][0]['artists'][0]['id']))

# #Data gen loop that will create the graph for pickling!
# first = 0
# for i in range(1500):

#     #pops first element in the queue
#     artist_name, artist_id = rec_queue.popleft()
#     if first < 5:
#         Recades_graph.firstInserts.append((artist_name, artist_id))
#         first += 1

#     print('Recommendations for ' + artist_name + ":")

#     #gets seed tracks from the artist
#     top_track_rec = requests.get(BASE_URL + 'artists/' + artist_id + '/top-tracks',
#     headers=headers,
#     params={
#         'id' : artist_id,
#         'market' : 'US'
#     }).json()

#     top_tracks = []
#     k = 0
#     for j in top_track_rec['tracks']:
#         if k == 5:
#             break
#         top_tracks.append(j['id'])
#         k += 1

#     #recommendations to add to queue from popped artist
#     recs = requests.get(BASE_URL + 'recommendations', headers=headers,
#     params={
#         'seed_artists' : artist_id,
#         'seed_tracks' : top_tracks,
#         'limit' : 5
#     }).json()

#     #passing artists as a (name, id) tuple for better traversal
#     for x in recs['tracks']:
#         Recades_graph.insert((artist_name, artist_id), (x['artists'][0]['name'], x['artists'][0]['id']))
#         rec_queue.append((x['artists'][0]['name'], x['artists'][0]['id']))
#         print(x['artists'][0]['name'])



outfile = open('RecadesGraph.p', 'wb')
pickle.dump(Recades_graph, outfile)
outfile.close()



#Creating trees that will be populated from the graph
#These trees will have node with degree 3 meaning
#that the maximum number of keys in nodes will be 3*2 - 1
sixties_tree = BTree(3)
seventies_tree = BTree(3)
eighties_tree = BTree(3)
nineties_tree = BTree(3)
thousands_tree = BTree(3)
tens_tree = BTree(3)


release_data_req = requests.get(BASE_URL + 'albums/' + '6tVg2Wl9hVKMpHYcAl2V2M',
        headers=headers,
        params={
            'id' : '6tVg2Wl9hVKMpHYcAl2V2M'
        }).json()


release_date = release_data_req['release_date']
release_date = release_date[:4]
data = int(release_date) % 100 // 10
print(str(data) + " " + release_date)

print('thanos')


#Adding the elements of the graphs into the appropriate decade tree
#This will be done by using a BFS traversal
visited = set()
queue = deque()
for x in Recades_graph.firstInserts:
    visited.add(x)
    queue.append(x)
        
    while queue:
        current = queue.pop()

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

        if data == 8:
            print(current)
            print(data)

        if data == 6:
            sixties_tree.insert([current, Recades_graph.adjList[current]])
        elif data == 7:
            seventies_tree.insert([current, Recades_graph.adjList[current]])
        elif data == 8:
            eighties_tree.insert([current, Recades_graph.adjList[current]])
        elif data == 9:
            nineties_tree.insert([current, Recades_graph.adjList[current]])
        elif data == 0:
            thousands_tree.insert([current, Recades_graph.adjList[current]])
        elif data == 1:
            tens_tree.insert([current, Recades_graph.adjList[current]])

        for neighbor in Recades_graph.adjList[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

print('roy disney')
