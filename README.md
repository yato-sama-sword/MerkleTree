# Overview
A Merkle tree implemented in Python3, which realized the functions of node searching, path checking and tree drawing.

The tree accepts a sorted and mapped hash array as input, and the elements in the array will be used as leaf nodes of the tree. 
We complete the hash operation on the array through hashlib
Each node of the tree has a key value to mark. For leaf nodes, this key value is the input hash value, and the key value of each internal node is equal to half of the sum of the values of its two child nodes. 
Therefore, this tree is equivalent to a binary search tree.

# Node Search
If the node exists, the path found to the node is returned.
Otherwise, they will be returned that the path of the node whose key value is just less than the node and whose key value is just greater than the node.
We search this path by finding the smaller node first and then the right one of the node.

# Path Checking
A simple search based on the input.

# Tree Drawing
Drawing based on graphviz.
