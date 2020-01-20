# KunduTree
A program that takes a tree and performs path analysis on it. Based on the problem Kundu and Tree from user amititkgp on Hackerrank.com.

# How to Use:
The program is contained in kundu.py which is programmed in Python 3. To use, download the file, make sure the python 3
interpreter is installed and then you can run this file from the command line with "python kundu.py <data.file>"

# Explanation of what it does:
The data file is a text file that contains the tree that is to be analyzed. It must be formatted with the first
line containing the number of nodes contained in the tree with each following line containing an edge to be added.
Each edge is a bidirectional connection between two nodes in the tree, and each edge has a color -- either red ('r') or black ('b').
data.txt is an example data file that creates the tree:
  1 <-b-> 2 <-r-> 3 <-r-> 4 <-b-> 5

The program then counts the number of tuples (t0, t1, t2) where t0, t1, and t2 are nodes in the tree and
there is at least one red edge in the path from t0 to t1 and at least one
red edge in the path between t1 and t2. For example, data.txt should return 4.
The tuples contained are (1, 3, 4), (2, 3, 4), (1, 3, 5), (2, 3, 5).
Note that different permutations of a tuple are not counted again.

The algorithm in kundu.py is essentially a modified Depth First Traversal of the given tree.
The tree is thought of as segments of black-edge connected nodes linked by red edges. The program selects
a leaf node in the tree and performs a depth first traversal of the tree separating segments of black-edged nodes
and once three segments exist in the path, then every time a new node is added, every possible set of tuples that
can be created with the first segment and the newest node are added to a set (s0) of sets (s1) where s1 is a set that
contains the nodes in a valid tuple. This is to prevent counting a single tuple multiple times because there are cases where
a tuple will appear multiple times. Essentially, this collects every valid tuple that can be made with the segment of black-edge
connected nodes that start with the initial leaf node selected. This node is now pruned from the tree, as well as all of the nodes
connected by a black edge to it. The pruning stops when a node with multiple branches is found or when a red edge is found.
The process is repeated with another leaf node until the tree is diminished to nothing. The final set of sets is counted and the total
number of valid tuples returned.

#Authors
John Horning (johnhorning@gmail.com)

#Copyright
Copyright 2020, John Horning, all rights reserved

This program is free to use or modify, but John Horning is not responsible for another's use of this code or 
the failure of this code in another program or context.

