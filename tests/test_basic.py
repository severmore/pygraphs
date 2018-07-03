import unittest
import bgraphs.graph

class TestProject(unittest.TestCase):
  """ Project existance test """

  def test_if_project_is_ok(self):
    assert True

class GraphCreationTestCase(unittest.TestCase):
  """ Test graph creation in different ways """

  EDGES_LIST = [ (0, 1), (0, 3), (1, 2), (2, 0), (2, 3), (3, 2) ]
  EDGES_INCIDENCE = [ [1, 3], [2], [0,3], [2] ]

  def test_empty_graph_creation(self):
    graph = bgraphs.graph.Graph()
    self.assertIsNotNone(graph)
    self.assertTrue(hasattr(graph, 'edges'))
    self.assertIsInstance(getattr(graph, 'edges'), list)
    self.assertEqual(graph.max_degree, 0)
  
  def test_graph_creation_by_specified_edges(self):
    graph = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, self.EDGES_INCIDENCE)
    self.assertEqual(graph.max_degree, 2)

  def test_graph_creation_by_specified_graph(self):
    graph_origin = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    graph = bgraphs.graph.Graph(graph=graph_origin)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, self.EDGES_INCIDENCE)
    self.assertNotEqual(graph, graph_origin)
    self.assertEqual(graph.max_degree, 2)
  
  def test_graph_creation_by_edges_and_graph_when_graph_has_more_vertices(self):
    graph_origin = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    graph = bgraphs.graph.Graph(edges=[(0, 2), (1, 0)], graph=graph_origin)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, [ [2, 1, 3], [0, 2], [0,3], [2] ])
    self.assertEqual(graph.max_degree, 3)
  
  def test_graph_creation_by_edges_and_graph_when_endes_has_more_vertices(self):
    graph_origin = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    graph = bgraphs.graph.Graph(edges=[(4, 0), (4, 2)], graph=graph_origin)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, [ [1, 3], [2], [0,3], [2], [0, 2] ])
    self.assertEqual(graph.max_degree, 2)
  
  def test_graph_creation_without_edges(self):
    graph = bgraphs.graph.Graph(vertices_num=5)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, [[], [], [], [], []])
    self.assertEqual(graph.max_degree, 0)
  
  def test_graph_creation_with_edges_and_vertices_specified_tight(self):
    graph = bgraphs.graph.Graph(edges=self.EDGES_LIST, vertices_num=4)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, self.EDGES_INCIDENCE)
    self.assertEqual(graph.max_degree, 2)

  def test_graph_creation_with_edges_and_vertices_specified_wide(self):
    graph = bgraphs.graph.Graph(edges=self.EDGES_LIST, vertices_num=5)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, self.EDGES_INCIDENCE + [[]])
    self.assertEqual(graph.max_degree, 2)
  
  def test_graph_creation_with_graph_and_vertices_specified_tight(self):
    graph_origin = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    graph = bgraphs.graph.Graph(graph=graph_origin, vertices_num=4)
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, self.EDGES_INCIDENCE)
    self.assertEqual(graph.max_degree, 2)


if __name__ == '__main__':
  unittest.main()
