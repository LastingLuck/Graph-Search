import unittest
from GraphSearch import GraphSearch


class TestBFS(unittest.TestCase):

    def setUp(self):
        self.graph_dir = "graphs/"
        self.test_path = []
        self.close_list = []
        self.search = GraphSearch()

    def tearDown(self):
        del self.search
        del self.test_path[:]
        del self.close_list[:]

    def test_bfs1(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'A')
        self.test_path = ['A']
        self.close_list = [['A', None]]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs2(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'B')
        self.test_path = ['A', 'B']
        self.close_list = [['A', None], ['B', 'A']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs3(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'C')
        self.test_path = ['A', 'C']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs4(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'D')
        self.test_path = ['A', 'D']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs5(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'E')
        self.test_path = ['A', 'B', 'E']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs6(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'F')
        self.test_path = ['A', 'C', 'F']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs7(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'G')
        self.test_path = ['A', 'C', 'F', 'G']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E'],
                           ['G', 'F']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs8(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'H')
        self.test_path = ['A', 'C', 'F', 'H']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E'],
                           ['G', 'F'], ['H', 'F']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs9(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'I')
        self.test_path = ['A', 'B', 'E', 'I']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs10(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'J')
        self.test_path = ['A', 'B', 'E', 'J']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs11(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'K')
        self.test_path = ['A', 'B', 'E', 'J', 'K']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E'],
                           ['G', 'F'], ['H', 'F'], ['M', 'I'], ['K', 'J']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs12(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'L')
        self.test_path = ['A', 'C', 'F', 'H', 'L']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E'],
                           ['G', 'F'], ['H', 'F'], ['M', 'I'], ['K', 'J'],
                           ['L', 'H']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs13(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'M')
        self.test_path = ['A', 'B', 'E', 'I', 'M']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E'],
                           ['G', 'F'], ['H', 'F'], ['M', 'I']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)

    def test_bfs14(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.bfs('A', 'N')
        self.test_path = ['A', 'B', 'E', 'I', 'M', 'N']
        self.close_list = [['A', None], ['B', 'A'], ['C', 'A'], ['D', 'A'],
                           ['E', 'B'], ['F', 'C'], ['I', 'E'], ['J', 'E'],
                           ['G', 'F'], ['H', 'F'], ['M', 'I'], ['K', 'J'],
                           ['L', 'H'], ['N', 'M']]
        # print self.search._close_list
        self.assertEquals(cmp(path, self.test_path), 0)
        self.assertEquals(cmp(self.search._close_list, self.close_list), 0)


if __name__ == '__main__':
    unittest.main()
