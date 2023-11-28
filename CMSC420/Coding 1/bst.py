import json
from typing import List

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self,
                  key        = None,
                  keycount   = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.keycount   = keycount
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "keycount": node.keycount,
            "leftchild": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root and the key given:
# If the key is not in the tree, insert it with a keycount of 1.
# If the key is in the tree, increment its keycount.
def insert(root: Node, key: int) -> Node:
    if root == None:
        root = Node()
        root.key = key
        root.keycount = 1
    elif root.leftchild != None and key < root.key:
        root.leftchild = insert(root.leftchild, key)
    elif root.rightchild != None and key > root.key:
        root.rightchild = insert(root.rightchild, key)
    elif root.leftchild == None and key < root.key:
        root.leftchild = Node()
        root.leftchild.key = key
        root.leftchild.keycount = 1
    elif root.rightchild == None and key > root.key:
        root.rightchild = Node()
        root.rightchild.key = key
        root.rightchild.keycount = 1
    else:
        root.keycount += 1
    return root

# For the tree rooted at root and the key given:
# If the key is not in the tree, do nothing.
# If the key is in the tree, decrement its key count. If they keycount goes to 0, remove the key.
# When replacement is necessary use the inorder successor.
def inorder_successor(root: Node) -> Node:
    successor = root.rightchild
    while successor != None and successor.leftchild != None:
        successor = successor.leftchild
    return successor

def delete(root: Node, key: int) -> Node:
    if root == None:
        root = None #Do Nothing
    elif key > root.key: 
        root.rightchild = delete(root.rightchild, key)
    elif key < root.key:
        root.leftchild = delete(root.leftchild, key)
    elif root.key == key:
        root.keycount -= 1
        if root.keycount <= 0:
            if root.leftchild == None and root.rightchild == None:
                root = None
            elif root.leftchild != None and root.rightchild == None:
                root = root.leftchild
            elif root.leftchild == None and root.rightchild != None:
                root = root.rightchild
            else:
                successor = root.rightchild
                while successor != None and successor.leftchild != None:
                    successor = successor.leftchild
                temp = root.key
                root.key = successor.key
                root.keycount = successor.keycount
                successor.keycount = 0
                successor.key = temp
                root.rightchild = delete(root.rightchild, successor.key)
    return root

# For the tree rooted at root and the key given:
# Calculate the list of keys on the path from the root towards the search key.
# The key is not guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    path = []
    node = root
    while node != None:
        path.append(node.key)
        if node.key == search_key:
            break
        elif search_key < node.key:
            node = node.leftchild
        elif search_key > node.key:
            node = node.rightchild
    return(json.dumps(path, indent = 2))

# For the tree rooted at root, find the preorder traversal.
# Return the json.dumps of the list with indent=2.
def preorderhelper(root: Node) -> list:
    if root == None:
        path = []
    else:
        path = [root.key]
        left_subtree = preorderhelper(root.leftchild)
        right_subtree = preorderhelper(root.rightchild)
        path = path + left_subtree
        path = path + right_subtree
    return path

def preorder(root: Node) -> str:
    path = preorderhelper(root)
    return(json.dumps(path, indent = 2))

# For the tree rooted at root, find the inorder traversal.
# Return the json.dumps of the list with indent=2.
def inorderhelper(root: Node) -> list:
    if root == None:
        path = []
    else:
        path = [root.key]
        left_subtree = inorderhelper(root.leftchild)
        right_subtree = inorderhelper(root.rightchild)
        path = left_subtree + path
        path = path + right_subtree
    return path

def inorder(root: Node) -> str:
    path = inorderhelper(root)
    return(json.dumps(path, indent = 2))

# For the tree rooted at root, find the postorder traversal.
# Return the json.dumps of the list with indent=2.

def postorderhelper(root: Node) -> list:
    if root == None:
        path = []
    else:
        path = [root.key]
        left_subtree = postorderhelper(root.leftchild)
        right_subtree = postorderhelper(root.rightchild)
        path = left_subtree + right_subtree + path
    return path

def postorder(root: Node) -> str:
    path = postorderhelper(root)
    return(json.dumps(path, indent = 2))

# For the tree rooted at root, find the BFT traversal (go left-to-right).
# Return the json.dumps of the list with indent=2.
def bft(root: Node) -> str:
    path = []
    queue = []
    if root != None:
        queue.append(root)
    
    while len(queue) > 0:
        root = queue.pop(0)
        if(root.leftchild != None):
            queue.append(root.leftchild)
        if(root.rightchild != None):
            queue.append(root.rightchild)
        path.append(root.key)
    return json.dumps(path, indent = 2)