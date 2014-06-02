# TODO - Implement uc_search, greedy_bfs, and a_star
# TODO - test load_graph, dfs, and bfs
# TODO - Update load_graph so it populates node_pos


import Queue
import math

# Dictionary containing a node as a key and a list of [node, cost] as the value
__graph = {}
# Dictionary containing a node and its position
__node_pos = {}
# Flag for the type of nodes (has cost/has position)
__have_cost = -1


def load_graph(file_name):
    if __graph:
        __graph.clear()
    file = open(file_name)
    data = file.read()
    parse_data(data)


# ---------------- #
# Search Functions #
# ---------------- #


def dfs(start, end):
    if not __graph:
        raise GraphError("No graph has been loaded")
    return dfs_helper(start, end, [])


def bfs(start, end):
    if not __graph:
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
            return make_path(end, closed_list)
        edges = __graph[next_node]
        for edge in edges:
            if edge[0] == end:
                print "Edge"
                print closed_list
                closed_list.append([edge[0], next_node])
                return make_path(end, closed_list)
            if not closed_list_contains(edge[0], closed_list):
                closed_list.append([edge[0], next_node])
                open_queue.put(edge[0])
        prev_node = next_node
    # No path found. Return empty list
    return []


def ucs(start, end):
    if not __graph:
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
            return make_path(end, closed_list)
        edges = __graph[next_node]
        for edge in edges:
            if edge[0] == end:
                closed_list.append([edge[0], next_node])
                return make_path(end, closed_list)
            if not closed_list_contains(edge[0], closed_list):
                closed_list.append([edge[0], next_node])
                total_cost = get_total_cost(edge[0], closed_list)
                open_queue.put((total_cost, edge[0]))
        prev_node = next_node
    return []


def gbfs(start, end):
    if not __graph:
        raise GraphError("No graph has been loaded")
    if __have_cost:
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
        if not closed_list_contains(next_node, closed_list):
            closed_list.append([next_node, prev_node])
        if next_node == end:
            return make_path(end, closed_list)
        successors = __graph[next_node]
        for edge in successors:
            if not closed_list_contains(edge[0], closed_list):
                h = get_h_cost(edge[0])
                open_queue.put((h, [edge[0], next_node]))
    return []


# def a_star(start, end):


# ---------------- #
# Helper Functions #
# ---------------- #

def dfs_helper(node, goal, path):
    # if we have reached to end, begin recursive fallback
    if node == goal:
        return [node]
    try:
        children = __graph[node]
        # Note: child is of the form [node, cost]
        for child in children:
            path = dfs_helper(child[0], goal, path)
            # goal was found, so add this node and return path
            if path:
                return [node] + path
    except KeyError:
        return []
    # goal not found in any of current nodes children, so return an empty list
    return []


# Goes in reverse order from the end through the closed list to form the path
def make_path(end, closed_list):
    print closed_list
    path = [end]
    next_item = get_next(end, closed_list)
    while next_item is not None:
        path = [next_item] + path
        next_item = get_next(next_item, closed_list)
    return path


# Grabs the next node from the closed list
def get_next(node, closed_list):
    for item in closed_list:
        if item[0] == node:
            return item[1]
    return None


# Checks the closed list to see if the passed node is in it
def closed_list_contains(node, closed_list):
    for item in closed_list:
        if item[0] == node:
            return True
    return False


def get_total_cost(node, closed_list):
    cost = 0
    prev_node = get_next(node, closed_list)
    while prev_node is not None:
        options = __graph[prev_node]
        for opt in options:
            if opt[0] == node:
                if __have_cost:
                    cost += opt[1]
                else:
                    cost += get_distance(prev_node, opt[0])
        node = prev_node
        prev_node = get_next(node)


def get_h_cost(node, goal):
    return get_distance(node, goal)


def get_distance(node1, node2):
    pos1 = __node_pos[node1]
    pos2 = __node_pos[node2]
    return math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))


# ----------- #
# Graph Parse #
# ----------- #


def parse_data(graph_data):
    global __have_cost
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
        else:
            raise NodeParseError("Connections must be '<->', '->', or '<-'")

        link = tok.split(split_by)
        nd = link[0]
        node_con = link[1].split(':')
        if len(node_con) == 2:
            if __have_cost == -1:
                __have_cost = 1
            if not __have_cost:
                raise NodeParseError("Nodes must all be of the same type")
            try:
                cost = int(node_con[1])
            except ValueError:
                cost = float(node_con[1])

            if connection != 0:
                if nd in __graph:
                    # append [Node, Cost] to the list of connected nodes
                    __graph[nd] += [[node_con[0], cost]]
                else:
                    __graph[nd] = [[node_con[0], cost]]
            if connection != 1:
                if node_con[0] in __graph:
                    __graph[node_con[0]] += [[nd, cost]]
                else:
                    __graph[node_con[0]] = [[nd, cost]]
        # Nodes have a position
        elif len(node_con) == 3:
            if __have_cost:
                if __have_cost == -1:
                    __have_cost = 0
                else:
                    raise NodeParseError("Nodes must be of the same type")
            try:
                x = int(node_con[1])
                y = int(node_con[2])
            except ValueError:
                x = float(node_con[1])
                y = float(node_con[2])

            if connection != 0:
                if nd in __graph:
                    __graph[nd] += [[node_con[0], x, y]]
                else:
                    __graph[nd] = [[node_con[0], x, y]]
                if nd in __node_pos:
                    raise NodeParseError("Nodes must have only one position")
                else:
                    __node_pos[nd] = [x, y]
            if connection != 1:
                if node_con[0] in __graph:
                    __graph[node_con[0]] += [[nd, x, y]]
                else:
                    __graph[node_con[0]] = [[nd, x, y]]
                if node_con[0] in __node_pos:
                    raise NodeParseError("Nodes must have only one position")
                else:
                    __node_pos[node_con[0]] = [x, y]


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
