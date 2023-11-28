import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

# subtreeheight
# returns the height of a tree
def subtreeheight(node: Node) -> int:
    if node == None:
        return 0
    height= max(subtreeheight(node.leftchild), subtreeheight(node.rightchild)) + 1
    return height

# balance
# returns the balance value of a node
def balance(node: Node) -> int:
    if node == None:
        return 0
    else:
        R = subtreeheight(node.rightchild)
        L = subtreeheight(node.leftchild)
        bal = R - L
        return bal

# BSTinsert
# Inserts pair into a tree without doing any balancing, as per a standard 
def BSTinsert(root: Node, key: int, word: str) -> Node:
    if root == None:
        root = Node(key, word, None, None)
    elif key < root.key and root.leftchild != None:
        root.leftchild = BSTinsert(root.leftchild, key, word)
    elif key < root.key and root.leftchild == None:
        root.leftchild = Node(key, word, None, None)
    elif key > root.key and root.rightchild != None:
        root.rightchild = BSTinsert(root.rightchild, key, word)
    elif key > root.key and root.rightchild == None:
        root.rightchild = Node(key, word, None, None)
    return root

# Rebalances the entire tree
def rebalance(root: Node) -> Node: 
    newroot = root
    rootBal = balance(root)
    # print("The balance of " + str(root.key) + " is: " + str(rootBal))
    leftBal = balance(root.leftchild)
    # print("     Left balance of " + str(root.key) + " is: " + str(leftBal))
    rightBal = balance(root.rightchild)
    # print("     Right balance of " + str(root.key) + " is: " + str(rightBal))

    if rootBal < -1:
        if leftBal < 0:
            # print("Right Rotation on: " + str(root.key))
            # Right Rotation
            LeftChild = root.leftchild
            LeftRightSubtree = LeftChild.rightchild
            root.leftchild = LeftRightSubtree
            LeftChild.rightchild = root
            newroot = LeftChild
        elif leftBal > 0:
            # print("Left-Right Rotation on: " + str(root.key))
            # Left-Right rotation
            LChild = root.leftchild
            LRChild = LChild.rightchild
            LRLChild = LRChild.leftchild
            #Left Rotation
            LChild.rightchild = LRLChild
            LRChild.leftchild = LChild
            root.leftchild = LRChild
            #Right Rotation
            root.leftchild = LRChild.rightchild
            LRChild.rightchild = root
            newroot = LRChild
    elif rootBal > 1:
        if rightBal > 0:
            # print("Left Rotation on: " + str(root.key))
            # Left Rotation
            RightChild = root.rightchild
            RightLeftSubtree = RightChild.leftchild
            root.rightchild = RightLeftSubtree
            RightChild.leftchild = root
            newroot = RightChild
        elif rightBal < 0:
            # print("Right-Left Rotation on: " + str(root.key))
            # Right-Left rotation
            RChild = root.rightchild
            RLChild = RChild.leftchild
            RLRChild = RLChild.rightchild

            RChild.leftchild = RLRChild
            RLChild.rightchild = RChild
            root.rightchild = RLChild

            root.rightchild = RLChild.leftchild
            RLChild.leftchild = root
            newroot = RLChild
    return newroot

def rebalance_path(root: Node, search_key: int) -> Node:
    if root == None:
        return 
    elif search_key < root.key:
        root.leftchild = rebalance_path(root.leftchild, search_key)
        root = rebalance(root)
        return root
    elif search_key > root.key:
        root.rightchild = rebalance_path(root.rightchild, search_key)
        root = rebalance(root)
        return root
    else:
        return rebalance(root)

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.

def insert(root: Node, key: int, word: str) -> Node:
    root = BSTinsert(root, key, word)
    root = rebalance_path(root, key)
    return root

def preorder(root: Node) -> list:
    if root == None:
        path = []
    else:
        path = [[root.key, root.word]]
        left_subtree = preorder(root.leftchild)
        right_subtree = preorder(root.rightchild)
        path = path + left_subtree
        path = path + right_subtree
    return path

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    for n in items:
        BSTinsert(root, int(n[0]), n[1])
    pre = preorder(root)
    root = None
    for n in pre:
        root = insert(root, int(n[0]), n[1])
    return root

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    pre = preorder(root)
    final = []
    for n in pre:
        if (n[0] in keys) == False:
            final.append(n)
    root = None
    for n in final:
        root = insert(root, n[0],n[1])
    return root

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    path = []
    node = root
    while node != None:
        path.append(node.key)
        if node.key == search_key:
            path.append(node.word)
            return (json.dumps(path, indent = 2))
        elif search_key < node.key:
            node = node.leftchild
        elif search_key > node.key:
            node = node.rightchild
    path.append(None)
    return (json.dumps(path, indent = 2))

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> None:
    node = root
    while node != None:
        
        if node.key == search_key:
            node.word = replacement_word
            return root
        elif search_key < node.key:
            node = node.leftchild
        elif search_key > node.key:
            node = node.rightchild
    return root