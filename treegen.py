import string
import profile


def get_graph(b=26, d=3):
    if b > 26:
        b = 26
    if b < 1:
        b = 1
    if d < 0:
        d = 0
    graph = {}
    char_list = string.ascii_uppercase
    graph_gen_rec(0, b, d, 'A', graph, char_list)
    for node in graph:
        l = graph[node]
        for i in range(len(l)):
            l[i] = [l[i]]
        graph[node] = l
    return graph


def graph_gen_rec(depth, b, d, current, graph, char_list):
    if depth == d:
        return
    suc_list = get_suc_list(b, current, char_list)
    graph[current] = suc_list
    for node in graph[current]:
        graph_gen_rec(depth+1, b, d, node, graph, char_list)


def get_suc_list(b, current, char_list):
    suc_list = [current for i in range(b)]
    for i in range(b):
        suc_list[i] += char_list[i]
    return suc_list


if __name__ == '__main__':
    print get_graph(3, 2)
    # b=10, d=5 - 111,111 nodes
    # b=18, d=5 - 2,000,719 nodes
    # b=16, d=5 - 1,118,481 nodes
    # print "=========================="
    # print "Branching - 5    Depth - 3"
    # print "156 Nodes"
    # print "=========================="
    # profile.run('get_graph(5, 3)')
    # print "=========================="
    # print "Branching - 7    Depth - 5"
    # print "x Nodes"
    # print "=========================="
    # profile.run('get_graph(7, 5)')
    # print "=========================="
    # print "Branching - 16    Depth - 5"
    # print "1,118,481 Nodes"
    # print "=========================="
    # profile.run('get_graph(16, 5)')
    # print "=========================="
    # print "Branching - 18    Depth - 5"
    # print "2,000,719 Nodes"
    # print "=========================="
    # profile.run('get_graph(18, 5)')
