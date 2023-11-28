from __future__ import annotations
import json
from typing import List
import math

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  values   : List[str] = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.values   = values
        self.children = children
        self.parent   = parent

# Returns true if node is overfull
def overfull(tree: Btree, node: Node) -> bool:
    if node == None:
        return False
    else:
        m = tree.m
        return (len(node.keys) >= m)
# Returns true if node will be overfull if added to
def full(tree: Btree, node: Node) -> bool:
    if node == None:
        return False
    else:
        m = tree.m
        return (len(node.keys) >= (m-1))

# Returns true if node is underfull
def underfull(tree: Btree, node: Node) -> bool:
    m = tree.m
    keycount = len(node.keys)
    if (node == tree.root):
        return keycount == 0
    else:
        return (keycount < math.ceil(m/2))
# Returns true if node will be underfull if keys are taken
def low(tree: Btree, node: Node) -> bool:
    m = tree.m
    keycount = len(node.keys)
    if (node == tree.root):
        return keycount == 1
    else:
        return (keycount <= math.ceil(m/2)) 

def check(tree: Btree, node: Node):
    if overfull(tree, node):
        parent = None
        has_left = False
        left_sibling = None
        has_right = False
        right_sibling = None
        
        #Node immediately splits if node is the root
        if node == tree.root:
            # print("\tSplit at the root ", node.keys)
            if len(node.keys) % 2 == 0:
                median_index = math.floor(len(node.keys)/2) - 1
            else:
                median_index = math.floor(len(node.keys)/2)
            
            new_root = Node([node.keys[median_index]], [node.values[median_index]], [], None)
            new_left = Node(node.keys[0:median_index], node.values[0:median_index], node.children[0:median_index+1], new_root)
            for n in new_left.children:
                    if (n != None):
                        n.parent = new_left
            new_right = Node(node.keys[median_index+1:len(node.keys)], node.values[median_index+1:len(node.values)], node.children[median_index+1:len(node.children)], new_root)
            for n in new_right.children:
                    if n != None:
                        n.parent = new_right
            new_root.children.insert(0, new_right)
            new_root.children.insert(0, new_left)

            tree.root = new_root
            # print("\tnew root is ", new_root.keys)
            # print("\tnew children are ", new_left.keys, " and ", new_right.keys)
        # Node has a parent and can be rotated
        else:
            parent = node.parent
            node_index = parent.children.index(node)
            if node_index > 0:
                has_left = True
                left_sibling = parent.children[node_index-1]
            if node_index < len(parent.children)-1:
                has_right = True
                right_sibling = parent.children[node_index+1]

            # Left Rotate
            if has_left and not full(tree,left_sibling):
                # print("\tleft rotation into ", left_sibling.keys)
                # if left_sibling == None:
                #     parent.children[node_index-1] = Node([],[],[None], parent)

                t = len(left_sibling.keys) + len(node.keys)

                while len(node.keys) > math.ceil(t/2):
                    left_sibling.keys.insert(len(left_sibling.keys), parent.keys[node_index-1])
                    left_sibling.values.insert(len(left_sibling.values), parent.values[node_index-1])
                    left_sibling.children.insert(len(left_sibling.children), node.children[0])
                    if left_sibling.children[len(left_sibling.children)-1] != None:
                        left_sibling.children[len(left_sibling.children)-1].parent = left_sibling
            
                    parent.keys[node_index-1] = node.keys[0]
                    parent.values[node_index-1] = node.values[0]

                    node.keys.pop(0)
                    node.values.pop(0)
                    node.children.pop(0)
                # print("\tupdated node is now ", node.keys)
                # print("\tupdated sibling is now ", left_sibling.keys)
                # print("\tupdated parent is now ", parent.keys)
                # print("\tlist of updated siblings: ")
                # for n in parent.children:
                #     print("\t\t",n.keys)
            # Right Rotate
            elif has_right and not full(tree, right_sibling):
                # print("\tright rotation into ", right_sibling.keys)
                # if right_sibling == None:
                #     parent.children[node_index+1] = Node([],[],[None], parent)                
                
                t = len(right_sibling.keys) + len(node.keys)

                while len(node.keys) > math.ceil(t/2):
                    right_sibling.keys.insert(0, parent.keys[node_index])
                    right_sibling.values.insert(0, parent.values[node_index])
                    right_sibling.children.insert(0, node.children[len(node.children)-1])
                    if right_sibling.children[len(right_sibling.children)-1] != None:
                        right_sibling.children[0].parent = right_sibling

                    parent.keys[node_index] = node.keys[len(node.keys)-1]
                    parent.values[node_index] = node.values[len(node.values)-1]

                    node.keys.pop(len(node.keys)-1)
                    node.values.pop(len(node.values)-1)
                    node.children.pop(len(node.children)-1)
                # print("\tupdated node is now ", node.keys)
                # print("\tupdated sibling is now ", right_sibling.keys)
                # print("\tupdated parent is now", parent.keys)
                # print("\tlist of updated siblings: ")
                # for n in parent.children:
                #     print("\t\t",n.keys)
            # Split
            else:
                # print("\tSplitting at node",node.keys)
                if len(node.keys) % 2 == 0:
                    median_index = math.floor(len(node.keys)/2) - 1
                else:
                    median_index = math.floor(len(node.keys)/2)
                
                new_left = Node(node.keys[0:median_index], node.values[0:median_index], node.children[0:median_index+1], parent)
                for n in new_left.children:
                    if (n != None):
                        n.parent = new_left
                new_right = Node(node.keys[median_index+1:len(node.keys)], node.values[median_index+1:len(node.values)], node.children[median_index+1:len(node.children)], parent)
                for n in new_right.children:
                    if n != None:
                        n.parent = new_right
                parent.keys.insert(node_index, node.keys[median_index])
                parent.values.insert(node_index, node.values[median_index])
                parent.children.pop(node_index)
                parent.children.insert(node_index, new_right)
                parent.children.insert(node_index, new_left)
                # print("\tnew children are ", new_left.keys, " and ", new_right.keys)
                # print("\tnew parent is ", new_left.parent.keys," = ", new_right.parent.keys," = ", parent.keys)
                # print("\tthe parent's children are: ")
                # for c in parent.children:
                #     print("\t\t",c.keys)
            if parent != None:
                check(tree, parent)

def d_check(tree: Btree, node: Node):
    print()

def search_helper(node: Node, key: int) -> list:
        List = []
        if node == None:
            return []
        for i in range(0,len(node.keys)):
            if key == node.keys[i]:
                return [node.values[i]]
            if i == len(node.keys)-1 and key > node.keys[i]:
                List.append(i+1)
                return List + search_helper(node.children[i+1], key)
            elif key < node.keys[i]:
                List.append(i)
                return List + search_helper(node.children[i], key)

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = root

    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "keys": node.keys,
                "values": node.values,
                "children": [(_to_dict(child) if child is not None else None) for child in node.children]
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert.
    def insert(self, key: int, value: str):
        node = self.root
        # print("inserting key ",key)
        if node == None:
            self.root = Node([key],[value], [None, None], None)
            node = self.root
            # print("inserted into node ", node.keys)
        else:
            while node != None: 
                for i in range(0, len(node.keys)):
                    if node.keys[i] > key:
                        if node.children[i] == None:
                            node.keys.insert(i,key)
                            node.values.insert(i,value)
                            node.children.insert(i, None)
                            # print("inserted into node ", node.keys)
                            check(self, node)
                            return
                        else:
                            node = node.children[i]
                            break
                    elif i == len(node.keys)-1 and key > node.keys[i]:
                        if node.children[i+1] == None:
                            node.keys.insert(i+1,key)
                            node.values.insert(i+1,value)
                            node.children.insert(i+2, None)
                            # print("inserted into node ", node.keys)
                            check(self, node)
                            return
                        else:
                            node = node.children[i+1]
                            break
        check(self, node)

    # Delete.
    def delete(self, key: int):
        node = self.root
        if node == None:
            return
        # print(f'Delete: {key}') # This is just here to make the code run, you can delete it.

    # Search
    def search(self,key) -> str:
        List = search_helper(self.root, key)
        return json.dumps(List)