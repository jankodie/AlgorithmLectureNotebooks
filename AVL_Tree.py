#%% [markdown]
# # Lecture 17 - AVL Trees
#%% [markdown]
# ## Definition

#%%
import sys
import random
import getopt

class AVLNode(object):
    """
    Binary tree node.
    """

    def __init__(self, key, lchild = None, rchild = None):
        self.key     = key
        self.lchild  = lchild
        self.rchild  = rchild
        self.balance = 0

    def recompute_balance(self):
        balance = height(self.lchild) - height(self.rchild)

class AVLTree(object):
    """
    Container type with the root of the tree.
    """
    def __init__(self):
        self.root = None

    def insert(self,key):
        #print "Inserting", key
        #print "-----------"
        #self.print_tree()
        #print "-----------"
        self.root, dummy = avl_insert(self.root, key)
        #print "-----------"
        #self.print_tree()
        #print "-----------"
        #print "Finished", key
        #print "==========="

    def insert_set(self, set, files=False):
        for k in set:
            self.insert(k)
            if files:
                dot_print_tree_full(self.root)

    def print_tree(self):
        print_tree(self.root)

    def find(self, key):
        return find(self.root, key)

#%% [markdown]
# ## Insert a Key

#%%
def avlrotate_rl(tree):
    tree.rchild, delta1 = avlrotate_r(tree.rchild)
    tree, delta2 = avlrotate_l(tree)
    return tree, delta1 + delta2

def avlrotate_lr(tree):
    tree.lchild, delta1 = avlrotate_l(tree.lchild)
    tree, delta2 = avlrotate_r(tree)
    return tree, delta1 + delta2

rtable = {
    (-1, 0) : ( 0,  1,  0),
    (-1,-1) : ( 1,  1,  0),
    (-1, 1) : ( 0,  2,  0),
    (-2,-1) : ( 0,  0, -1),
    (-2,-2) : ( 1,  0, -1)}

def avlrotate_r(tree):
    pivot = tree.lchild
    tbal = tree.balance
    pbal = pivot.balance
    tree.lchild = pivot.rchild
    pivot.rchild = tree
    tree.balance, pivot.balance, delta = rtable[(tbal,pbal)]
    print("L: (%2d,%2d) => (%2d, %2d, %2d)"%(tbal, pbal, tree.balance, pivot.balance, delta))
    return pivot, delta

ltable = {
    ( 1, 0) : ( 0, -1,  0),
    ( 1, 1) : (-1, -1,  0),
    ( 1,-1) : ( 0, -2,  0),
    ( 2, 1) : ( 0,  0, -1),
    ( 2, 2) : (-1,  0, -1)}

def avlrotate_l(tree):
    pivot = tree.rchild
    tbal = tree.balance
    pbal = pivot.balance
    tree.rchild = pivot.lchild
    pivot.lchild = tree
    tree.balance, pivot.balance, delta = ltable[(tbal,pbal)]
    print("L: (%2d,%2d) => (%2d, %2d, %2d)"%(tbal, pbal, tree.balance, pivot.balance, delta))
    return pivot, delta


def avl_insert(tree, key):
    """
    Insert a key into the tree. Return tupel of new tree and change in
    height (1 or 0).
    """
    if not tree:
        return AVLNode(key), 1
    elif key < tree.key:
        tree.lchild, delta = avl_insert(tree.lchild, key)
        if delta:
            tree.balance = tree.balance - delta
            if tree.balance == -2:
                print("Rebalance left", tree.key)
                if tree.lchild.balance <= 0:
                    print("left-left")
                    tree, delta = avlrotate_r(tree)
                else:
                    print("left-right", tree.key)
                    tree,delta = avlrotate_lr(tree)
                # We know from theoretical analyis that the tree depth
                # does not grow here
                return tree, 0
            else:
                # branch has possibly grown deeper
                return tree, abs(tree.balance)
        else:
            return tree, 0
    elif key > tree.key:
        tree.rchild, delta = avl_insert(tree.rchild, key)
        if delta:
            tree.balance = tree.balance+delta
            if tree.balance == 2:
                print("Rebalance right", tree.key)
                if tree.rchild.balance >= 0:
                    print("right-right", tree.key)
                    tree, delta = avlrotate_l(tree)
                else:
                    print("right-left", tree.key)
                    tree,delta = avlrotate_rl(tree)
                return tree, 0
            else:
                # branch has possibly grown deeper
                return tree, abs(tree.balance)
        else:
                # We know from theoretical analyis that the tree depth
                # does not grow here
            return tree, 0
    else:
        print("Error: Duplicate key")
        return tree, 0
    
keys = [16, 55, 19, 68, 72, 21, 33, 28, 15, 11, 40]
tree = AVLTree()
tree.insert_set(keys, False)


#%%
def tree_height(tree):
    if tree:
        return 1 + max(tree_height(tree.lchild), tree_height(tree.rchild))
    else:
        return 0

def tree_bal(tree):
    if tree:
        return tree_height(tree.rchild) - tree_height(tree.lchild)
    return 0

def find(tree, key):
    if tree:
        if key < tree.key:
            return find(tree.lchild, key)
        if key > tree.key:
            return find(tree.rchild, key)
        return tree

def print_tree(tree, indent = ""):
    if tree:
        print_tree(tree.lchild, indent + "  ")
        bal = tree_height(tree.rchild) - tree_height(tree.lchild)
        marker = ""
        if bal!=tree.balance:
            marker = "!"
        print("%s:%2d:%2d:%3d:%s %s"%(marker, tree.balance, bal, tree_height(tree), indent, tree.key))
        print_tree(tree.rchild, indent+"  ")

tree.print_tree()
#%%
tree.print_tree()
print("---------------------------")
tree.insert(25)
tree.print_tree()
print("---------------------------")
tree.insert(23)
tree.print_tree()
#%% [markdown]
# ## First Task
# Build the tree with labels ranging from 1 to 7:
#%%
keys1 = list(range(1,8))
tree1 = AVLTree()
tree1.insert_set(keys1, False)
tree1.print_tree()
#%% [markdown]
# Add labels 9 and 8 to this tree:

#%%
tree1.print_tree()
print("---------- Insert 9 -----------")
tree1.insert(9)
tree1.print_tree()
print("---------- Insert 8 -----------")
tree1.insert(8)
tree1.print_tree()

#%%
