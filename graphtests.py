import GraphSearch
import unittest


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph_dir = "graphs/"
        self.test_graph = {}

    def tearDown(self):
        self.test_graph.clear()

    def test_graph1(self):
        self.test_graph
        GraphSearch.load_graph(self.graph_dir + "graph1.txt")
        self.test_graph['A'] = [['B', 1]]
        self.test_graph['B'] = [['C', 2]]
        self.test_graph['C'] = [['D', 3]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)
        # print("Graph1 test passed")

    def test_graph2(self):
        GraphSearch.load_graph(self.graph_dir + "graph2.txt")
        self.test_graph['A'] = [['B', 1], ['E', 16]]
        self.test_graph['B'] = [['C', 2]]
        self.test_graph['C'] = [['D', 3], ['E', 4]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)
        # print("Graph2 test passed")

    def test_graph3(self):
        GraphSearch.load_graph(self.graph_dir + "graph3.txt")
        self.test_graph['A'] = [['B', 1]]
        self.test_graph['B'] = [['C', 2]]
        self.test_graph['C'] = [['D', 3], ['E', 4]]
        self.test_graph['E'] = [['A', 16]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)
        # print("Graph3 test passed")

    def test_graph4(self):
        GraphSearch.load_graph(self.graph_dir + "graph4.txt")
        self.test_graph['A'] = [['B', 1], ['E', 16]]
        self.test_graph['B'] = [['A', 1], ['C', 2]]
        self.test_graph['C'] = [['D', 3], ['E', 4]]
        self.test_graph['D'] = [['C', 3]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)
        # print("Graph4 test passed")

    def test_graph5(self):
        GraphSearch.load_graph(self.graph_dir + "graph5.txt")
        self.test_graph['A'] = [['B', 5], ['C', 5], ['D', 6]]
        self.test_graph['B'] = [['E', 5]]
        self.test_graph['C'] = [['E', 6], ['F', 4]]
        self.test_graph['D'] = [['F', 4]]
        self.test_graph['E'] = [['I', 5], ['J', 5]]
        self.test_graph['F'] = [['G', 2], ['H', 5]]
        self.test_graph['G'] = [['K', 5]]
        self.test_graph['H'] = [['L', 4]]
        self.test_graph['I'] = [['M', 3]]
        self.test_graph['J'] = [['M', 4], ['K', 4]]
        self.test_graph['K'] = [['M', 3], ['N', 4]]
        self.test_graph['L'] = [['N', 4]]
        self.test_graph['M'] = [['N', 7]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)
        # print("Graph5 test passed")

    def test_graph6(self):
        GraphSearch.load_graph(self.graph_dir + "graph6.txt")
        self.test_graph['A'] = [['B', 1, 1]]
        self.test_graph['B'] = [['C', 2, 2]]
        self.test_graph['C'] = [['D', 3, 3], ['E', 4, 4]]
        self.test_graph['E'] = [['A', 1, 1]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)

    def test_graph7(self):
        GraphSearch.load_graph(self.graph_dir + "graph7.txt")
        self.test_graph['A'] = [['B', 1, 1], ['E', 4, 1]]
        self.test_graph['B'] = [['C', 2, 3]]
        self.test_graph['C'] = [['D', 3, 4], ['E', 4, 1]]
        self.assertEqual(cmp(self.test_graph, GraphSearch._graph), 0)

if __name__ == '__main__':
    unittest.main()