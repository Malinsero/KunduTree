# A program that takes a tree with N vertices and N - 1 edges. These edges can be red or black. Given a tree,
# find the number of valid tuples (0, 1, 2) such that there is at least one red edge between t[0] and t[1]
# and at least one red edge between t[1] and t[2]. Note that (0, 1, 2) is the same as (1, 0, 2) or any other
# permutation.
#
# This program uses a DFT of sorts to find the valid tuples and counts them.
# The input for this program is to run it from command line with the name of a .txt file as the input.
# The format of the file is an integer N representing the number of nodes on the first line, and on subsequent lines,
# an integer representing the first node's index, a space, an integer representing the second node's index, a space,
# and a char either 'r' or 'b' to represent red or black.
# i.e.
# 4
# 1 2 r
# 2 3 r
# 3 4 b
# represents the graph:  1 r-> 2 r-> 3 b-> 4
# which would evaluate to 2 valid tuples.
#
# @author John Horning (johnhorning@gmail.com)
# @version December 21, 2019

import sys


# Create a data structure that represents a single node in the graph
class Node:
    def __init__(self):
        self.last_edge = False  # variable that holds true if all the edges have been traversed
        self.edge_idx = 0  # variable that keeps the index of whatever edge is currently being used.
        self.edges = []
        return

    # Method that takes the id of the node being edged to and a boolean representing whether the edge is red
    # adds the node edge to this node and increments the number of edges this node contains
    def add_edge(self, node_id, color):
        self.edges.append((node_id, color))  # add the edge as a tuple
        return

    # Method that takes the id of a node and removes it if it is in this node.
    def remove_edge(self, node_id):
        for tup in range(len(self.edges)):  # for each edge in the node
            if self.edges[tup][0] == node_id:  # if this is the right edge
                self.edges.pop(tup)  # remove it
                return

    # Method that dumps all the edges from a node
    def clear_edges(self):
        self.edges.clear()
        return

    # Method that returns this node's next edge for the dft. If all the edges have been returned
    # then it will return False, otherwise, it will return the edge.
    def next_edge(self):

        if self.last_edge:  # if all the edges have been traversed
            self.last_edge = False  # set last edge to false
            return False  # return that the edges have been traversed.

        edge = self.edges[self.edge_idx]  # grab the next edge to return
        self.edge_idx += 1  # increment the edge to be returned next

        # Check if that was the last edge to return, and if it was reset the node
        if self.edge_idx >= len(self.edges):
            self.edge_idx = 0
            self.last_edge = True

        return edge  # return the edge


class Graph:

    # Create an instance of the graph that is large enough to store 'size' nodes
    def __init__(self, size):
        self.nodes = dict.fromkeys(range(1, size + 1))
        return

    # Method takes two nodes and the color of their edge and adds it to the graph
    def add_edge(self, node1, node2, color):
        if self.nodes[node1] is None:  # if the first node has not been added yet
            self.nodes[node1] = Node()  # add it

        if self.nodes[node2] is None:  # if the second node has not been added yet
            self.nodes[node2] = Node()

        # add this edge to both nodes
        self.nodes[node1].add_edge(node2, color)
        self.nodes[node2].add_edge(node1, color)
        return

    # Method takes a node's index and removes the node and all edges involving it from the graph
    def remove_node(self, idx):
        for edge in self.nodes[idx].edges:  # for each edge in node
            self.nodes[edge[0]].remove_edge(idx)  # remove this node from the nodes that connect to it

        self.nodes[idx].clear_edges()  # remove all the nodes edges
        self.nodes.pop(idx)  # remove the node from the graph
        return

    # Method takes the index of a node that has only one edge and removes
    # its entire branch from the graph unless it his a red edge
    # stops after removing a node right before a red edge or before a branch
    def prune(self, idx):
        if len(self.nodes[idx].edges) != 1:  # if this node has more than one edge
            return

        if self.nodes[idx].edges[0][1]:  # If the node's edge is red
            self.remove_node(idx)
            return

        current = self.nodes[idx].edges[0][0]  # set the next node to the next node in the path
        self.remove_node(idx)  # remove the originally entered node
        self.prune(current)  # recursively continue with the next node
        return


# Function that iteratively solves a DFT. returns a set of triplets that account for all triplets
# within the tree that satisfy the requirements of the problem.
def dft(idx, tree):
    visited = dict.fromkeys(tree.nodes.keys(), False)  # create a dictionary of visited nodes with the default val false

    triplets = set()  # a set to hold the triplets
    segments = [[]]  # a list to hold the subsets of the path
    cur_seg = 0  # variable that tracks the current segment
    segments[cur_seg].append(idx)  # add this node to the path
    visited[idx] = True  # mark the node as visited

    while True:  # While there are still nodes in the path
        current_edge = tree.nodes[segments[cur_seg][-1]].next_edge()  # grab the next edge from the path's last node

        if not current_edge:  # if that node has already given all its edges
            segments[cur_seg].pop()  # Remove this node from the path. it's done.
            if not len(segments[cur_seg]):  # if this segment is now empty
                if cur_seg == 0:  # if this was the last segment
                    return triplets  # return the sets found

                # If there are more segments
                cur_seg -= 1  # move to one segment prior
            continue  # if a node has been popped of the path, then move to the next iteration

        if visited[current_edge[0]]:  # if this node has already been visited
            continue  # move to the next iteration
        else:  # if this node has not been visited
            visited[current_edge[0]] = True  # mark it as visited

        if current_edge[1]:  # if this edge is red and thus starts a new segment
            cur_seg += 1  # move to the next edge
            if len(segments) <= cur_seg:  # if another segment does not already exist to use this path
                segments.append([])  # append another segment

        segments[cur_seg].append(current_edge[0])  # add this node's index to the current path.

        # If there are enough segments, construct all possible tuples containing this node:
        if cur_seg >= 2:  # If there are three or more segments
            for node_idx in segments[0]:  # for each node in the first segment
                for seg_idx in range(1, cur_seg):  # for each segment between the first and last
                    for node2_idx in segments[seg_idx]:  # for each node in the segment in the middle
                        triplets.add(frozenset([node_idx, node2_idx, current_edge[0]]))  # add the  triplet to the set


# Function that takes a bidirectional tree with red and black edges and solves the problem
def solve(tree):
    triplets = set()  # create a set that will hold the triplets. triplets are also represented as sets
    boolreturn = False  # a value used in the while loop to continue if the for loop took action.

    while True:  # continue to iterate until the graph is gone.

        # start by finding an index of a node with only one edge. Start the DFT
        for idx in tree.nodes.keys():  # for each index-node pair in the graph
            if len(tree.nodes[idx].edges) == 1:  # when a proper node is found
                triplets.update(dft(idx, tree))  # perform the dft on the graph
                tree.prune(idx)  # prune this branch from the tree
                boolreturn = True  # make the while loop continue
                break  # break from the for loop and iterate through the while again.

        if boolreturn:  # if the while loop needs to continue
            boolreturn = False  # reset the boolean
            continue  # move to the next iteration

        return len(triplets)  # if we leave the for loop, we are done. Return


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python kundu.py [.txt file name]")
        exit(1)

    try:
        fptr = open(sys.argv[1])  # open the incoming file for reading.
        print("File " + sys.argv[1] + " opened. Reading...")
    except IOError:
        print("File failed to open. Program Exiting...")
        exit(1)

    try:
        num_nodes = int(fptr.readline())  # get the number of nodes from the file
        my_tree = Graph(num_nodes)  # create the graph with enough nodes to support the incoming file.
        for i in range(num_nodes - 1):  # for each edge being inputted
            edge = fptr.readline().rstrip('\n').split(' ')  # get the next edge from the file
            my_tree.add_edge(int(edge[0]), int(edge[1]), 'r' == str(edge[2]))  # add the edge to the tree
    except IOError:
        print("Error encountered getting data from the given file. Program Exiting...")
        exit(1)

    fptr.close()  # close the file provided.

    print("Tree created. Solving...")

    total = solve(my_tree)  # solve the kundu tree.
    print("Number of tuples: " + str(total))  # print the result to the user.
