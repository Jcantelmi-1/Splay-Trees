from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# Performs a left rotation on a node (parent node's perspective)
def left_rotate(node: Node)-> Node:
    if node == None:
        return None
    RightChild = node.rightchild
    RightLeftSubtree = RightChild.leftchild

    node.rightchild = RightLeftSubtree
    if RightLeftSubtree != None:
        RightLeftSubtree.parent = node
    RightChild.leftchild = node
    RightChild.parent = node.parent
    if node.parent != None and node.parent.leftchild == node:
        node.parent.leftchild = RightChild
    elif node.parent != None and node.parent.rightchild == node:
        node.parent.rightchild = RightChild
    node.parent = RightChild
    return RightChild

# Performs a right rotation on a node (parent nodes's perspective)
def right_rotate(node: Node) -> Node:
    if node == None:
        return None
    LeftChild = node.leftchild
    LeftRightSubtree = LeftChild.rightchild

    node.leftchild = LeftRightSubtree
    if LeftRightSubtree != None:
        LeftRightSubtree.parent = node
    LeftChild.rightchild = node
    LeftChild.parent = node.parent
    if node.parent != None and node.parent.leftchild == node:
        node.parent.leftchild = LeftChild
    elif node.parent != None and node.parent.rightchild == node:
        node.parent.rightchild = LeftChild
    node.parent = LeftChild
    return LeftChild

# Finds the target node
def find_target(node: Node, key: int) -> Node:
    if key < node.key and node.leftchild != None:
        return find_target(node.leftchild, key)
    elif key > node.key and node.rightchild != None:
        return find_target(node.rightchild, key)
    else:
        return node

# ONLY SPLAYS THE EXACT Key. Cannot automatically find IOS or IOP, 
# that's what the find_closest function is for. Therefore, assume key
# is always inside the tree. If key < node.key then that node must have
# a left child. 

def splay_step(target: Node) -> Node:
    while target.parent != None:
        if target.parent.parent == None:
            if target == target.parent.leftchild:
                target = right_rotate(target.parent)
                return target
            elif target == target.parent.rightchild:
                target = left_rotate(target.parent)
                return target
        else:
            if target == target.parent.leftchild and target.parent == target.parent.parent.leftchild:
                target.parent = right_rotate(target.parent.parent)
                target = right_rotate(target.parent)
            elif target == target.parent.rightchild and target.parent == target.parent.parent.leftchild:
                target = left_rotate(target.parent)
                target = right_rotate(target.parent)
            elif target == target.parent.leftchild and target.parent == target.parent.parent.rightchild:
                target = right_rotate(target.parent)
                target = left_rotate(target.parent)
            elif target == target.parent.rightchild and target.parent == target.parent.parent.rightchild:
                target.parent = left_rotate(target.parent.parent)
                target = left_rotate(target.parent)
    return target

def splay(root: Node, key: int) -> Node:
    target = find_target(root, key)
    target = splay_step(target)
    return target

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Search
    def search(self,key:int):
        root = self.root
        if root != None:
            root = splay(root,key)
            self.root = root


    # Insert Method 1
    def insert(self,key:int):
        root = self.root 
        if root == None:
            root = Node(key, None, None, None)
            self.root = root
        else:
            root = splay(root, key)
            if key > root.key:
                new_root = Node(key, root, root.rightchild, None)
                root.parent = new_root
                if root.rightchild != None:
                    root.rightchild.parent = new_root
                root.rightchild = None
                self.root = new_root
            elif root.key > key:
                new_root = Node(key, root.leftchild, root, None)
                root.parent = new_root
                if root.leftchild != None:
                    root.leftchild.parent = new_root
                root.leftchild = None
                self.root = new_root


    # Delete Method 1
    def delete(self,key:int):
        root = self.root
        if root == None:
            return
        root = splay(root, key)
        if root.leftchild != None and root.rightchild != None:
            root.rightchild = splay(root.rightchild, key)
            root.rightchild.leftchild = root.leftchild
            root.rightchild.leftchild.parent = root.rightchild
            root.rightchild.parent = None
            self.root = root.rightchild
        elif root.leftchild != None and root.rightchild == None:
            root.leftchild.parent = None
            self.root = root.leftchild
        elif root.leftchild == None and root.rightchild != None:
            root.rightchild.parent = None
            self.root = root.rightchild
        else:
            self.root = None