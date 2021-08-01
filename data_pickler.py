import pickle
import requests
import json
from requests.models import HTTPBasicAuth

class BTreeNode:
    def __init__(self, leaf=False, degree=0):
        self.leaf = False
        self.keys = []
        self.child = []
        self.number = 0
        self.degree = degree

    def split(self, index, c):

        key_storage = BTreeNode(c.degree, c.leaf)
        key_storage.number = c.degree - 1

        for i in range(self.degree -1):
            key_storage.keys[i] = c.keys[i+self.degree]

        #copying the last 'degree' children of c to key_storage
        if c.leaf == False:
            for i in range(0, self.degree):
                key_storage.child[i] = c.child[i+self.degree]
        
        #cutting down the number of keys in c
        c.number = self.degree - 1

        #self is going to receive new child
        #space will be made
        for i in range(self.number, index, -1):
            self.child[i+1] = self.child[i]
        
        #linking new child to self
        self.child[index+1] = key_storage

        #moving c keys to self and rearranging
        for i in range(self.number, index - 1, -1):
            self.keys[i+1] = self.keys[i]
        
        #middle key of c will go to this node
        self.keys[index] = c.keys[self.degree - 1]

        #Increment key count of self
        self.number += 1

class BTree:
    def __init__(self, minDegree):
        self.root = BTreeNode(True)
        self.minDegree = minDegree


    def insert(self, key):
        if self.root == None:
            self.root = BTreeNode(True, self.t)
            self.root.keys.append(key)
            self.root.number += self.root.number
        else:
            #this is so fun!
            if self.root.number == 2*self.minDegree - 1:
                #making a new root
                node = BTreeNode(False, self.minDegree)

                #old root is child of new root
                node.child.append(self.root)

                #split old root
                


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

sixties_graph = Graph()
seventies_graph = Graph()
eighties_graph = Graph()
nineties_graph = Graph()
thousands_graph = Graph()
tens_graph = Graph()

sixties_tree = BTree()
seventies_tree = BTree()
eighties_tree = BTree()
nineties_tree = BTree()
thousands_tree = BTree()
tens_tree = BTree()

