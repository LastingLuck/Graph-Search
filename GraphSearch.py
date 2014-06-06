# Line Format:
#     Node1<connection>Node2:Cost
#     Can remove cost and put (x,y) instead
#     Can do that for both sides. E.g. Node1(x,y)<conn.>Node2(x,y)
#     Node position can be done before or after node links
#       Node1=(x,y)       Node1->Node2
#       Node2=(a,b)   ==  Node1=(x,y)   ==   Node1(x,y)->Node2(a,b)
#       Node1->Node2      Node2=(a,b)

# TODO - Implement a_star
# TODO - test load_graph, dfs, bfs, usc, gbfs
# TODO - Trim the graph stuff to allow for spaces in file

# Possible flags:
#   (for init, searches) Manhatten Distance instead of straight-line distance
#   (for set_graph) Flag to disable graph checking
#   (for loads, init) Set seperator value

import Queue
import math
import re

# Dictionary containing a node as a key and a list of [node, cost] as the value
# If nodes have a position the graph will contain [node, x, y] or [node]
# _graph = {}
# Dictionary containing a node and its position
# _node_pos = {}
# Flag for the type of nodes (has cost/has position)
# _have_cost = -1


class GraphSearch:
    '''
    Python class for doing graph searches. Graphs are loaded
    from file or from a string.

    <conn.> can be '<->', '->', or '<-'
    Graph format for nodes with cost:
        * Node1<conn.>Node2:Cost
    Graph formats for nodes with position:
            ***Note: Braces means it's optional***
        * Node1<conn.>Node2:x:y[:z]
        * Node1:x:y[:z]<conn.>Node2:x:y[:z]
        * Node1<conn.>Node2(x,y[,z])
        * Node1(x,y[,z])<conn.>Node2(x,y[,z])
        * Node1<conn.>Node2
          Node1=(x,y[,z])
          Node2=(x,y[,z])
        * Node1=(x,y[,z])
          Node2=(x,y[,z])
          Node1<conn.>Node2

    Format for the graph (used for set_graph):
        graph = {node: [[conn_node1, cost/pos],[conn_node2, cost/pos],...],...}
            * If the nodes have a position, including them here is optional.
              Positions will be taken from the node_pos dictionary and not
              here. The list would then look like [[node1], [node2], ...].
              They're still each in their own list for compatability reasons.
        node_pos = {node: [x, y(, z)], ...}
            ***Note: Parentheses mean optional here(braces already taken)***
        * The cost/position parts of the 2 dictionaries can be in string form.
          They're automatically converted to int or float.

    Heuristic used for gbfs, and a* is the straight line distance between node
    and goal. In the future there will be a flag to allow the use of manhatten
    distance instead.
    '''
    def __init__(self, data=None):
        self._graph = {}
        self._node_pos = {}
        self._have_cost = None
        if data is not None:
            if '\n' in data:
                self.load_graph(data)
            else:
                self.load_from_file(data)

    def load_from_file(self, file_name):
        '''
        Loads a graph from the file specified
        '''
        graph = open(file_name)
        data = graph.read()
        self.load_graph(data)
        graph.close()

    def load_graph(self, data_str):
        '''
        Loads a graph from the string specified
        '''
        if self._graph:
            self._graph.clear()
        if self._node_pos:
            self._node_pos.clear()
        self._have_cost = None
        self._parse_data(data_str)

    def set_graph(self, graph, pos=None):
        '''
        Set function for the graph. Takes in a dictionary containing the nodes
        and a list of the connnected nodes. If nodes have positions, then
        another dictionary of nodes and their positions is passes in. For more
        detail see the documentation.
        '''
        self._graph = self._valid_graph(graph)
        if pos is not None:
            self._node_pos = self._valid_pos(pos)

# ---------------- #
# Search Functions #
# ---------------- #

    def dfs(self, start, end):
        '''
        Performs a depth-first search on the currently loaded graph.
        Caution: Get's stuck in loops very easily
        '''
        if not self._graph:
            raise self.GraphError("No graph has been loaded")
        return self._dfs_helper(start, end, [])

    def bfs(self, start, end):
        '''
        Performs a breadth-first search on the currently loaded graph.
        '''
        if not self._graph:
            raise self.GraphError("No graph has been loaded")
        closed_list = []
        open_queue = Queue.Queue()
        open_queue.put(start)
        closed_list.append([start, None])
        prev_node = None

        while not open_queue.empty():
            next_node = open_queue.get()
            if next_node == end:
                print "Node"
                print closed_list
                closed_list.append([next_node, prev_node])
                return self._make_path(end, closed_list)
            edges = self._graph[next_node]
            for edge in edges:
                if edge[0] == end:
                    print "Edge"
                    print closed_list
                    closed_list.append([edge[0], next_node])
                    return self._make_path(end, closed_list)
                if not self._closed_list_contains(edge[0], closed_list):
                    closed_list.append([edge[0], next_node])
                    open_queue.put(edge[0])
            prev_node = next_node
        # No path found. Return empty list
        return []

    def ucs(self, start, end):
        '''
        Preforms a uniform cost search on the currently loaded graph
        '''
        if not self._graph:
            raise self.GraphError("No graph has been loaded")
        closed_list = []
        open_queue = Queue.PriorityQueue()
        open_queue.put((0, start))
        closed_list.append([start, None])
        prev_node = None

        while not open_queue.empty():
            next_node = open_queue.get()
            if next_node[1] == end:
                closed_list.append([next_node, prev_node])
                return self._make_path(end, closed_list)
            edges = self._graph[next_node]
            for edge in edges:
                if edge[0] == end:
                    closed_list.append([edge[0], next_node])
                    return self._make_path(end, closed_list)
                if not self._closed_list_contains(edge[0], closed_list):
                    closed_list.append([edge[0], next_node])
                    total_cost = self._get_total_cost(edge[0], closed_list)
                    open_queue.put((total_cost, edge[0]))
            prev_node = next_node
        return []

    def gbfs(self, start, end):
        '''
        Performs a greedy best first search on the currently loaded graph.
        The straight-line distance is used for the heuristic value.
        Loaded graph must have positions associated with the nodes and not cost
        '''
        if not self._graph:
            raise self.GraphError("No graph has been loaded")
        if self._have_cost:
            raise self.SearchError("Nodes must have positions instead of cost")
        closed_list = []
        open_queue = Queue.PriorityQueue()
        open_queue.put((0, [start, None]))
        closed_list.append([start, None])
        prev_node = None
        # prev_h_val = None

        while not open_queue.empty():
            best_node = open_queue.get()
            next_node = best_node[0]
            prev_node = best_node[1]
            if not self._closed_list_contains(next_node, closed_list):
                closed_list.append([next_node, prev_node])
            if next_node == end:
                return self._make_path(end, closed_list)
            successors = self._graph[next_node]
            for edge in successors:
                if not self._closed_list_contains(edge[0], closed_list):
                    h = self._get_h_cost(edge[0])
                    open_queue.put((h, [edge[0], next_node]))
        return []

    # def a_star(start, end):

# ---------------- #
# Helper Functions #
# ---------------- #

    def _dfs_helper(self, node, goal, path):
        '''
        Function that's called recursively for the depth-first search.
        '''
        # if we have reached to end, begin recursive fallback
        if node == goal:
            return [node]
        try:
            children = self._graph[node]
            # Note: child is of the form [node, cost]
            for child in children:
                path = self._dfs_helper(child[0], goal, path)
                # goal was found, so add this node and return path
                if path:
                    return [node] + path
        except KeyError:
            return []
        # goal not found in any of current nodes children, return an empty list
        return []

    def _make_path(self, end, closed_list):
        '''
        Makes a path from the end node to the start by going through the
        closed list in reverse order
        '''
        print closed_list
        path = [end]
        next_item = self._get_next(end, closed_list)
        while next_item is not None:
            path = [next_item] + path
            next_item = self._get_next(next_item, closed_list)
        return path

    # Grabs the next node from the closed list
    def _get_next(self, node, closed_list):
        for item in closed_list:
            if item[0] == node:
                return item[1]
        return None

    # Checks the closed list to see if the passed node is in it
    def _closed_list_contains(self, node, closed_list):
        for item in closed_list:
            if item[0] == node:
                return True
        return False

    def _get_total_cost(self, node, closed_list):
        '''
        Gets the actual cost of what it took to get to the current node.
        Does not account for the heuristic value.
        '''
        cost = 0
        prev_node = self._get_next(node, closed_list)
        while prev_node is not None:
            options = self._graph[prev_node]
            for opt in options:
                if opt[0] == node:
                    if self._have_cost:
                        cost += opt[1]
                    else:
                        cost += self._get_distance(prev_node, opt[0])
            node = prev_node
            prev_node = self._get_next(node)

    def _get_h_cost(self, node, goal):
        '''
        Returns the heuristic value of a node. This is currently the
        straight line distance between there and the end.
        '''
        return self._get_distance(node, goal)

    def _get_distance(self, node1, node2):
        '''
        Returns the distance between 2 nodes. Used for getting the actual cost
        and the heuristic cost.
        '''
        pos1 = self._node_pos[node1]
        pos2 = self._node_pos[node2]
        xdist = pos1[0] - pos2[0]
        ydist = pos1[1] - pos2[1]
        zdist = pos1[2] - pos2[2]
        return math.sqrt((ydist ** 2) + (xdist ** 2) + (zdist ** 2))

# ----------- #
# Graph Parse #
# ----------- #

    def _parse_data(self, graph_data):
        '''
        Parses the string gathered from the file into a graph
        '''
        # tokenize it
        tokens = graph_data.split('\n')
        for tok in tokens:
            # Skip comment and blank lines
            tok = tok.strip()
            if tok == "" or tok[0] == '#':
                continue
            # determine which type of connection it is
            if '<->' in tok:
                connection = 2
                split_by = '<->'
            elif '->' in tok:
                connection = 1
                split_by = '->'
            elif '<-' in tok:
                connection = 0
                split_by = '<-'
            elif '=' in tok:
                connection = -1
                split_by = '='
            else:
                raise self.NodeParseError("Connections must be '<->', '->',"
                                          " '<-', '='")

            # print tok
            link = tok.split(split_by)
            # If current line is a position assignment
            if connection == -1:
                # Regex split by ':', '(', ',', ')'
                pos = re.split(':|\(|\,|\)', link[1])
                # regex expression can lead to empty items at front/back
                if pos[len(pos)-1] == '':
                    pos.pop()
                if pos[0] == '':
                    pos.pop(0)
                pos[0] = pos[0].trim()
                pos[1] = pos[1].trim()
                # Attempt to convert the string to numbers. First attempt
                # int, then float.
                try:
                    # print pos
                    x = int(pos[0])
                    y = int(pos[1])
                except ValueError:
                    try:
                        x = float(pos[0])
                        y = float(pos[1])
                    except ValueError:
                        raise self.NodeParseError("Nodes have non-number"
                                                  " cost/pos")
                # Check if the node is already in the position dict and if so,
                # check if the current value is different this assignment.
                link[0] = link[0].trim()
                if (link[0] in self._node_pos) and \
                        (self._node_pos[link[0]] != [x, y]):
                    raise self.NodeParseError("Nodes must have only one"
                                              " postition")
                else:
                    self._node_pos[link[0]] = [x, y]
                # Skip the rest. Don't want to put everything below in an else
                continue
            # TODO - Figure out a better way to match node(x,y) pattern
            # Check if there is a cost or position for the left node
            if self._matches_format(link[0]):
                # Split the left side
                temp = re.split(':|\(|\,|\)', link[0])
                if temp[len(temp)-1] == '':
                    temp.pop()
                link[0] = temp[0].trim()
                temp[1] = temp[1].trim()
                temp[2] = temp[2].trim()
                # Attempt to convert to numbers
                try:
                    x = int(temp[1])
                    y = int(temp[2])
                except ValueError:
                    try:
                        x = float(temp[1])
                        y = float(temp[2])
                    except ValueError:
                        raise self.NodeParseError("Nodes have non-number"
                                                  " cost/pos")
                # Check if it's already in pos dict and if the current value
                # is different
                if temp[0] in self._node_pos and \
                        self._node_pos[temp[0]] != [x, y]:
                    raise self.NodeParseError("Nodes must have only one "
                                              "position")
                else:
                    self._node_pos[temp[0]] = [x, y]
            nd = link[0]
            # Split the right side
            node_con = re.split(':|\(|\,|\)', link[1])
            node_con[0] = node_con[0].trim()
            if node_con[len(node_con)-1] == '':
                node_con.pop()
            # Check if there is no node cost or position (node1<conn.>node2)
            if len(node_con) == 1:
                # Assign Flag. True-Nodes have cost. False-Nodes have position
                if self._have_cost:
                    if self._have_cost is None:
                        self._have_cost = False
                    else:
                        raise self.NodeParseError("Nodes must all be of "
                                                  "the same type")
                # Left to right connection
                if connection != 0:
                    if nd in self._graph:
                        self._graph[nd] += [[node_con[0]]]
                    else:
                        self._graph[nd] = [[node_con[0]]]
                # Right to left connection
                if connection != 1:
                    if node_con[0] in self._graph:
                        self._graph[node_con[0]] += [[nd]]
                    else:
                        self._graph[node_con[0]] = [[nd]]
            # Check if nodes have a cost
            if len(node_con) == 2:
                node_con[1] = node_con[1].trim()
                # Assign flag. True-Nodes have cost. False-Nodes have position
                if self._have_cost is None:
                    self._have_cost = True
                    # print("set have_cost to %d", _have_cost)
                    # print link
                    # print node_con
                if not self._have_cost:
                    raise self.NodeParseError("Nodes must all be of the"
                                              " same type")
                # Try to convert the cost/pos to numbers
                try:
                    cost = int(node_con[1])
                except ValueError:
                    try:
                        cost = float(node_con[1])
                    except ValueError:
                        raise self.NodeParseError("Nodes have non-number"
                                                  " cost/pos")
                # Left to right connection
                if connection != 0:
                    if nd in self._graph:
                        # append [Node, Cost] to the list of connected nodes
                        self._graph[nd] += [[node_con[0], cost]]
                    else:
                        self._graph[nd] = [[node_con[0], cost]]
                # Right to left connection
                if connection != 1:
                    if node_con[0] in self._graph:
                        self._graph[node_con[0]] += [[nd, cost]]
                    else:
                        self._graph[node_con[0]] = [[nd, cost]]
            # Nodes have a position
            elif len(node_con) >= 3:
                node_con[1] = node_con[1].trim()
                node_con[2] = node_con[2].trim()
                # If len > 4 then there's too many entries. Only first 3 count,
                # the rest are ignored
                # Set flags. True-Nodes have cost. False-Nodes have position
                if self._have_cost:
                    if self._have_cost is None:
                        self._have_cost = False
                    else:
                        raise self.NodeParseError("Nodes must be of the "
                                                  "same type")
                try:
                    x = int(node_con[1])
                    y = int(node_con[2])
                    if len(node_con) == 4:
                        z = int(node_con[3].trim())
                    else:
                        z = 0
                except ValueError:
                    try:
                        x = float(node_con[1])
                        y = float(node_con[2])
                        if len(node_con) == 4:
                            z = float(node_con[3].trim())
                        else:
                            z = 0
                    except ValueError:
                        raise self.NodeParseError("Nodes have non-number"
                                                  " cost/pos")
                # Left to right connection
                if connection != 0:
                    if nd in self._graph:
                        self._graph[nd] += [[node_con[0], x, y, z]]
                    else:
                        self._graph[nd] = [[node_con[0], x, y, z]]
                    if (node_con[0] in self._node_pos) and \
                            (self._node_pos[node_con[0]] != [x, y, z]):
                        # print _node_pos[node_con[0]]
                        # print [x, y]
                        raise self.NodeParseError("Nodes must have only"
                                                  " one position")
                    else:
                        self._node_pos[node_con[0]] = [x, y, z]
                # Right to left connection
                if connection != 1:
                    if node_con[0] in self._graph:
                        self._graph[node_con[0]] += [[nd, x, y, z]]
                    else:
                        self._graph[node_con[0]] = [[nd, x, y, z]]
                    if nd in self._node_pos and \
                            self._node_pos[nd] != [x, y, z]:
                        raise self.NodeParseError("Nodes must have only"
                                                  " one position")
                    else:
                        self._node_pos[nd] = [x, y, z]

    def _matches_format(self, string):
        '''
        Wether or not the string matches the format "a(b,c[,d])
        '''
        flag = 0
        for i in range(len(string)):
            if string[i] == '(':
                if flag == 0:
                    flag += 1
                else:
                    return False
            if string[i] == ',':
                if flag == 1 or flag == 2:
                    flag += 1
                else:
                    return False
            if string[i] == ')':
                if flag == 2 or flag == 3:
                    return True
                else:
                    return False
        return False

    def _valid_graph(self, graph):
        '''
        Checks wether or not the graph is in the correct format
        '''
        if not isinstance(graph, dict):
            raise self.GraphError("Graph is not a dictionary")
        try:
            for node in graph:
                edges = graph[node]
                for edge in edges:
                    if not isinstance(edge, list):
                        raise self.GraphError("Graph edges are not in a list")
                    if len(edge) > 3:
                        raise self.GraphError("Graph entries have too many "
                                              "entries")
                    if len(edge) == 0:
                        raise self.GraphError("Graph has empty entries")
                    if not isinstance(edge[1], (int, float, long)):
                        try:
                            edge[1] = int(edge[1])
                        except ValueError:
                            edge[1] = float(edge[1])
                        except:
                            raise self.GraphError("Graph has non-number"
                                                  " values")
                    if not isinstance(edge[2], (int, float, long)):
                        try:
                            edge[2] = int(edge[2])
                        except ValueError:
                            edge[2] = float(edge[2])
                        except:
                            raise self.GraphError("Graph has non-number"
                                                  " values")
        except KeyError:
            raise self.GraphError("General Error in testing graph validity")
        return graph

    def _valid_pos(self, pos):
        if not isinstance(pos, dict):
            raise self.GraphError("Position list is not a dictionary")
        try:
            for node in pos:
                loc = pos[node]
                if not isinstance(loc, list):
                    raise self.GraphError("Node Position Entries are not in a"
                                          " list")
                if len(loc) > 3:
                    raise self.GraphError("Node Position entries have too many"
                                          " entries")
                if len(loc) < 2:
                    raise self.GraphError("Node Position entries have too few"
                                          " entries")
                if not isinstance(loc[0], (int, float, long)):
                    try:
                        loc[0] = int(loc[0])
                    except ValueError:
                        try:
                            loc[0] = float(loc[0])
                        except:
                            raise self.GraphError("Node Position has "
                                                  "non-number values")
                if not isinstance(loc[1], (int, float, long)):
                    try:
                        loc[1] = int(loc[1])
                    except ValueError:
                        try:
                            loc[1] = float(loc[1])
                        except:
                            raise self.GraphError("Node Position has "
                                                  "non-number values")
        except KeyError:
            raise self.GraphError("General Error in testing node position"
                                  " validity")
        return pos

# ------------- #
# Custom Errors #
# ------------- #

    class NodeParseError(Exception):
        '''
        Exception that is raised during the parsing of the data into the graph"
        '''
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class SearchError(Exception):
        '''
        Expection that is raised during the searches
        '''
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class GraphError(Exception):
        '''
        More general exception. Raised if issue with the graph during the
        search and if there is an issue in the set_graph function
        '''
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)
