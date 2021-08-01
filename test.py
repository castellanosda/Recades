import pickle

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

infile = open("pickled_tree.p", "rb")
tree = pickle.load(infile)
infile.close()

tree.inorder(tree.root)