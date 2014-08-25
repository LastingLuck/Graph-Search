# from GraphSearch import GraphSearch
import treegen
import profile


print "Running Tests"
print "=========================="
print "Branching - 5    Depth - 3"
print "156 Nodes"
print "=========================="
profile.run('get_graph(5, 3)')
print "=========================="
print "Branching - 7    Depth - 5"
print "x Nodes"
print "=========================="
profile.run('get_graph(7, 5)')
print "=========================="
print "Branching - 16    Depth - 5"
print "x Nodes"
print "=========================="
profile.run('get_graph(16, 5)')
print "=========================="
print "Branching - 18    Depth - 5"
print "x Nodes"
print "=========================="
profile.run('get_graph(18, 5)')
