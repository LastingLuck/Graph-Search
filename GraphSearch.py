# Line Format:
#     Node1<connection>Node2:Cost
#     Can remove cost and put (x,y) instead
#     Can do that for both sides. E.g. Node1(x,y)<conn.>Node2(x,y)
#     Node position can be done before or after node links
#       Node1=(x,y)       Node1->Node2
#       Node2=(a,b)   ==  Node1=(x,y)   ==   Node1(x,y)->Node2(a,b)
#       Node1->Node2      Node2=(a,b)

# TODO - Implement, gbfs and a_star
# TODO - test load_graph, dfs, bfs, and usc


import Queue
import math
import re

# Dictionary containing a node as a key and a list of [node, cost] as the value
# If nodes have a position the graph will contain [node, x, y] or [node]
_graph = {}
# Dictionary containing a node and its position
_node_pos = {}
# Flag for the type of nodes (has cost/has position)
_have_cost = -1


def load_graph(file_name):
    '''
    Loads a graph from the file specified
    '''
    if _graph:
        _graph.clear()
    if _node_pos:
        _node_pos.clear()
    global _have_cost
    _have_cost = -1
    graph = open(file_name)
    data = graph.read()
    parse_data(data)
    graph.close()


# ---------------- #
# Search Functions #
# ---------------- #


def dfs(start, end):
    '''
    Performs a depth-first search on the currently loaded graph.
    '''
    if not _graph:
        raise GraphError("No graph has been loaded")
    return _dfs_helper(start, end, [])


def bfs(start, end):
    '''
    Performs a breadth-first search on the currently loaded graph.
    '''
    if not _graph:
        raise GraphError("No graph has been loaded")
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
            return _make_path(end, closed_list)
        edges = _graph[next_node]
        for edge in edges:
            if edge[0] == end:
                print "Edge"
                print closed_list
                closed_list.append([edge[0], next_node])
                return _make_path(end, closed_list)
            if not _closed_list_contains(edge[0], closed_list):
                closed_list.append([edge[0], next_node])
                open_queue.put(edge[0])
        prev_node = next_node
    # No path found. Return empty list
    return []


def ucs(start, end):
    '''
    Preforms a uniform cost search on the currently loaded graph
    '''
    if not _graph:
        raise GraphError("No graph has been loaded")
    closed_list = []
    open_queue = Queue.PriorityQueue()
    open_queue.put((0, start))
    closed_list.append([start, None])
    prev_node = None

    while not open_queue.empty():
        next_node = open_queue.get()
        if next_node[1] == end:
            closed_list.append([next_node, prev_node])
            return _make_path(end, closed_list)
        edges = _graph[next_node]
        for edge in edges:
            if edge[0] == end:
                closed_list.append([edge[0], next_node])
                return _make_path(end, closed_list)
            if not _closed_list_contains(edge[0], closed_list):
                closed_list.append([edge[0], next_node])
                total_cost = _get_total_cost(edge[0], closed_list)
                open_queue.put((total_cost, edge[0]))
        prev_node = next_node
    return []


def gbfs(start, end):
    '''
    Performs a greedy best first search on the currently loaded graph.
    The straight-line distance is used for the heuristic value.
    Loaded graph must have positions associated with the nodes and not weights
    '''
    if not _graph:
        raise GraphError("No graph has been loaded")
    if _have_cost:
        raise SearchError("Nodes must have positions instead of cost for gbfs")
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
        if not _closed_list_contains(next_node, closed_list):
            closed_list.append([next_node, prev_node])
        if next_node == end:
            return _make_path(end, closed_list)
        successors = _graph[next_node]
        for edge in successors:
            if not _closed_list_contains(edge[0], closed_list):
                h = _get_h_cost(edge[0])
                open_queue.put((h, [edge[0], next_node]))
    return []


# def a_star(start, end):


# ---------------- #
# Helper Functions #
# ---------------- #

def _dfs_helper(node, goal, path):
    # if we have reached to end, begin recursive fallback
    if node == goal:
        return [node]
    try:
        children = _graph[node]
        # Note: child is of the form [node, cost]
        for child in children:
            path = _dfs_helper(child[0], goal, path)
            # goal was found, so add this node and return path
            if path:
                return [node] + path
    except KeyError:
        return []
    # goal not found in any of current nodes children, so return an empty list
    return []


# Goes in reverse order from the end through the closed list to form the path
def _make_path(end, closed_list):
    print closed_list
    path = [end]
    next_item = _get_next(end, closed_list)
    while next_item is not None:
        path = [next_item] + path
        next_item = _get_next(next_item, closed_list)
    return path


# Grabs the next node from the closed list
def _get_next(node, closed_list):
    for item in closed_list:
        if item[0] == node:
            return item[1]
    return None


# Checks the closed list to see if the passed node is in it
def _closed_list_contains(node, closed_list):
    for item in closed_list:
        if item[0] == node:
            return True
    return False


def _get_total_cost(node, closed_list):
    cost = 0
    prev_node = _get_next(node, closed_list)
    while prev_node is not None:
        options = _graph[prev_node]
        for opt in options:
            if opt[0] == node:
                if _have_cost:
                    cost += opt[1]
                else:
                    cost += _get_distance(prev_node, opt[0])
        node = prev_node
        prev_node = _get_next(node)


def _get_h_cost(node, goal):
    return _get_distance(node, goal)


def _get_distance(node1, node2):
    pos1 = _node_pos[node1]
    pos2 = _node_pos[node2]
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


# ----------- #
# Graph Parse #
# ----------- #


def parse_data(graph_data):
    '''
    Parses the string gathered from the file into a graph
    '''
    global _have_cost
    # tokenize it
    tokens = graph_data.split('\n')
    for tok in tokens:
        # Skip comment lines
        tok = tok.strip()
        if tok == "" or tok[0] == '#':
            continue

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
            raise NodeParseError("Connections must be '<->', '->', '<-', '='")

        # print tok
        link = tok.split(split_by)
        if connection == -1:
            pos = re.split(':|\(|\,|\)', link[1])
            if pos[len(pos)-1] == '':
                pos.pop()
            if pos[0] == '':
                pos.pop(0)
            try:
                # print pos
                x = int(pos[0])
                y = int(pos[1])
            except ValueError:
                x = float(pos[0])
                y = float(pos[1])
            if (link[0] in _node_pos) and (_node_pos[link[0]] != [x, y]):
                raise NodeParseError("Nodes must have only one postition")
            else:
                _node_pos[link[0]] = [x, y]
            continue
        # TODO - Figure out a better way to match node(x,y) pattern
        if _matches_format(link[0]):
            temp = re.split(':|\(|\,|\)', link[0])
            if temp[len(temp)-1] == '':
                temp.pop()
            link[0] = temp[0]
            try:
                x = int(temp[1])
                y = int(temp[2])
            except ValueError:
                x = float(temp[1])
                y = float(temp[2])
            if temp[0] in _node_pos and _node_pos[temp[0]] != [x, y]:
                raise NodeParseError("Nodes must have only one position")
            else:
                _node_pos[temp[0]] = [x, y]
        nd = link[0]
        node_con = re.split(':|\(|\,|\)', link[1])
        if node_con[len(node_con)-1] == '':
            node_con.pop()
        if len(node_con) == 1:
            if _have_cost:
                if _have_cost == -1:
                    _have_cost = 0
                else:
                    raise NodeParseError("Nodes must all be of the same type")
            if connection != 0:
                if nd in _graph:
                    _graph[nd] += [[node_con[0]]]
                else:
                    _graph[nd] = [[node_con[0]]]
            if connection != 1:
                if node_con[0] in _graph:
                    _graph[node_con[0]] += [[nd]]
                else:
                    _graph[node_con[0]] = [[nd]]
        if len(node_con) == 2:
            if _have_cost == -1:
                _have_cost = 1
                # print("set have_cost to %d", _have_cost)
                # print link
                # print node_con
            if not _have_cost:
                raise NodeParseError("Nodes must all be of the same type")
            try:
                cost = int(node_con[1])
            except ValueError:
                cost = float(node_con[1])

            if connection != 0:
                if nd in _graph:
                    # append [Node, Cost] to the list of connected nodes
                    _graph[nd] += [[node_con[0], cost]]
                else:
                    _graph[nd] = [[node_con[0], cost]]
            if connection != 1:
                if node_con[0] in _graph:
                    _graph[node_con[0]] += [[nd, cost]]
                else:
                    _graph[node_con[0]] = [[nd, cost]]
        # Nodes have a position
        elif len(node_con) == 3:
            # print tok
            # print node_con
            if _have_cost:
                if _have_cost == -1:
                    _have_cost = 0
                else:
                    raise NodeParseError("Nodes must be of the same type")
            try:
                x = int(node_con[1])
                y = int(node_con[2])
            except ValueError:
                x = float(node_con[1])
                y = float(node_con[2])

            if connection != 0:
                if nd in _graph:
                    _graph[nd] += [[node_con[0], x, y]]
                else:
                    _graph[nd] = [[node_con[0], x, y]]
                if (node_con[0] in _node_pos) and \
                        (_node_pos[node_con[0]] != [x, y]):
                    # print _node_pos[node_con[0]]
                    # print [x, y]
                    raise NodeParseError("Nodes must have only one position")
                else:
                    _node_pos[node_con[0]] = [x, y]
            if connection != 1:
                if node_con[0] in _graph:
                    _graph[node_con[0]] += [[nd, x, y]]
                else:
                    _graph[node_con[0]] = [[nd, x, y]]
                if nd in _node_pos and _node_pos[nd] != [x, y]:
                    raise NodeParseError("Nodes must have only one position")
                else:
                    _node_pos[nd] = [x, y]


def _matches_format(string):
    flag = 0
    for i in range(len(string)):
        if string[i] == '(':
            if flag == 0:
                flag = 1
            else:
                return False
        if string[i] == ',':
            if flag == 1:
                flag = 2
            else:
                return False
        if string[i] == ')':
            if flag == 2:
                return True
            else:
                return False
    return False

# ------------- #
# Custom Errors #
# ------------- #


class NodeParseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SearchError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GraphError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
