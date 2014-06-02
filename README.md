# README #

### What is this repository for? ###

This repo is for the python code for doing graph searches.

### How do I get set up? ###

Graphs are defined in plain text and are in the following format:


'Node1'<connection>'Node2':<cost/position>


Node1/2 are replaced with whatever you wish to name your nodes.

<connection> is replaced with either '<->', '->', or '<-' depending on how the nodes are connected

    * <-> is a 2-way connection. Ex. A<->B (A is connected to B and B is connected to A)
    * -> is a 1-way right connection. Ex. A->B (A is connected to B and B is not connected to A)
    * <- is a 1-way left connection. Ex. A<-B (A is not connected to B and B is connected to A)


If you want the links between nodes to have a cost, then <cost/position> is replaced with any number (int or float).


If you want each node to have a position, then <cost/position> is replaced with 2 numbers (int or float) in the format 'x:y'

    * As of now, any node that does not have a node connecting to it will have a position 0,0

    * The use of the 2-way connection assigns the position to the node on the right.

    * The use of the 1-way left connection will assign the position to the node on the left

### Plans ###
    * Come up with a format that allows for assigning positions to nodes on both sides
    * Implementing searches. (Currently only dfs, bfs, ucs, gbfs, and a* are planned)

### Status ###
Loading Graph - Basic Done. Needs Testing

DFS - Basic Done. Needs Testing

BFS - Basic Done. Needs Testing

UCS - Basic Done. Needs Testing

GBFS - Started Implementation. Not Yet Finished

A* - Not Yet Started