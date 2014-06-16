import unittest
from GraphSearch import GraphSearch


class TestDFS(unittest.TestCase):

    def setUp(self):
        self.graph_dir = "graphs/"
        self.test_path = []
        self.search = GraphSearch()

    def tearDown(self):
        del self.search
        del self.test_path[:]

    def test_dfs1(self):
        self.search.load_from_file(self.graph_dir + "graph1.txt")
        path = self.search.dfs('A', 'D')
        self.test_path = ['A', 'B', 'C', 'D']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs2(self):
        self.search.load_from_file(self.graph_dir + "graph2.txt")
        path = self.search.dfs('A', 'E')
        self.test_path = ['A', 'B', 'C', 'E']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs3(self):
        self.search.load_from_file(self.graph_dir + "graph2.txt")
        path = self.search.dfs('A', 'D')
        self.test_path = ['A', 'B', 'C', 'D']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs4(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'A')
        self.test_path = ['A']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs5(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'B')
        self.test_path = ['A', 'B']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs6(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'C')
        self.test_path = ['A', 'C']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs7(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'D')
        self.test_path = ['A', 'D']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs8(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'E')
        self.test_path = ['A', 'B', 'E']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs9(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'F')
        self.test_path = ['A', 'C', 'F']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs10(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'G')
        self.test_path = ['A', 'C', 'F', 'G']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs11(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'H')
        self.test_path = ['A', 'C', 'F', 'H']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs12(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'I')
        self.test_path = ['A', 'B', 'E', 'I']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs13(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'J')
        self.test_path = ['A', 'B', 'E', 'J']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs14(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'K')
        self.test_path = ['A', 'B', 'E', 'J', 'K']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs15(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'L')
        self.test_path = ['A', 'C', 'F', 'H', 'L']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs16(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'M')
        self.test_path = ['A', 'B', 'E', 'I', 'M']
        self.assertEquals(cmp(path, self.test_path), 0)

    def test_dfs17(self):
        self.search.load_from_file(self.graph_dir + "graph5.txt")
        path = self.search.dfs('A', 'N')
        self.test_path = ['A', 'B', 'E', 'I', 'M', 'N']
        self.assertEquals(cmp(path, self.test_path), 0)

if __name__ == '__main__':
    unittest.main()
