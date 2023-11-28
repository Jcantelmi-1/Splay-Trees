from typing import List

class Node():
    def  __init__(self,
                  key        = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild

def search(node: Node, search_key: int) -> bool:
    if node == None:
        return False
    elif search_key < node.key:
        return search(node.leftchild, search_key)
    elif search_key > node.key:
        return search(node.rightchild, search_key)
    else:
        return True

def insert(node: Node, new_key: int) -> Node:
    if node == None: 
        return Node(new_key, None, None)
    elif new_key < node.key and node.leftchild == None:
        node.leftchild = insert(node.leftchild, new_key)
    elif new_key > node.key and node.rightchild == None:
        node.rightchild = insert(node.rightchild, new_key)
    return node

def delete(node: Node, delete_key: int) -> Node:
    if node == None:
        return
    elif delete_key < node.key:
        node.leftchild = delete(node.leftchild, delete_key)
    elif delete_key > node.key:
        node.rightchild = delete(node.rightchild, delete_key)
    else:
        if node.leftchild == None and node.rightchild == None:
            return None
        elif node.leftchild != None and node.rightchild == None:
            return node.leftchild
        elif node.leftchild == None and node.rightchild != None:
            return node.rightchild
        else:
            successor = node.rightchild
            while successor != None and successor.leftchild != None:
                successor = successor.leftchild
            temp = node.key
            node.key = successor.key
            successor.key = temp
            node.rightchild = delete(node.rightchild, successor.key)



