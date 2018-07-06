import unittest
import bgraphs.graph
import bgraphs.tools
import bgraphs.coloring
import bgraphs.generating

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


class RemoveAddGraphTestCase(unittest.TestCase):

  def setUp(self):
    edges = [ (0, 1), (0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 2) ]
    self.graph = bgraphs.graph.Graph(edges=edges)

  def test_removing_edge(self):
    edges_ref = [ (0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 2) ]
    edgeslist_ref = bgraphs.graph.Graph(edges=edges_ref).edges
    self.graph.remove_edge(0, 1)
    self.assertListEqual(self.graph.edges, edgeslist_ref)

  def test_addition_edge(self):
    edges_ref = [ (0, 1), (0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 2),
                  (3, 2) ]
    edgeslist_ref = bgraphs.graph.Graph(edges=edges_ref).edges
    self.graph.add_edge(3, 2)
    self.assertListEqual(self.graph.edges, edgeslist_ref)


class GraphUnionTestCase(unittest.TestCase):
  
  def setUp(self):
    edges1 = [ (0, 1), (0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 2) ]
    edges2 = [ (3, 1), (0, 2)]
    self.graph1 = bgraphs.graph.Graph(edges=edges1)
    self.graph2 = bgraphs.graph.Graph(edges=edges2)

  def test_graph_union(self):
    edges_ref = [[1, 3, 2], [0, 2], [0, 3], [2, 1]]
    self.graph1.union(self.graph2)
    self.assertListEqual(self.graph1.edges, edges_ref)



class RemoveAddUDGraphTestCase(unittest.TestCase):

  def setUp(self):
    edges = [ (0, 1), (0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 2) ]
    self.udgraph = bgraphs.graph.UDGraph(edges=edges)

  def test_removing_edge(self):
    edges_ref = [ (0, 3), (1, 2), (2, 0), (2, 3), (3, 2) ]
    edgeslist_ref = bgraphs.graph.UDGraph(edges=edges_ref).edges
    self.udgraph.remove_edge(0, 1)
    self.assertListEqual(self.udgraph.edges, edgeslist_ref)

  def test_addition_edge(self):
    edges_ref = [ (0, 1), (0, 3), (1, 0), (1, 2), (2, 0), (2, 3), (3, 2),
                  (3, 2), (2, 3) ]
    edgeslist_ref = bgraphs.graph.UDGraph(edges=edges_ref).edges
    self.udgraph.add_edge(3, 2)
    self.assertListEqual(self.udgraph.edges, edgeslist_ref)


@unittest.skip('Skip for performance sake')
class VisingColoringTestCase(unittest.TestCase):

  def validate_edge_coloring(self, coloring, graph):
    """ Check if edge coloring is valid. """

    print(graph)
    print(coloring)
    
    for start, incidents in enumerate(graph.edges):
      colorset = { coloring[start, end] for end in incidents }
      
      if len(colorset) != len(graph.edges[start]):
        return False
    
    return True
    

  def test_vising_simple(self):
    EDGES = [(0,2), (0,3), (1,2), (1,3), (2,0), (2,1), (3,0), (3,1)]
    graph = bgraphs.graph.Graph(edges=EDGES)
    coloring = bgraphs.coloring.colorize(graph)
    self.assertTrue(self.validate_edge_coloring(coloring, graph))
  
  def test_vising_generated(self):
    graph = bgraphs.generating.bgraph(20, vratio_low=.4, vratio_high=.6, 
                                      edge_prob=0.3)
    coloring = bgraphs.coloring.colorize(graph)
    self.assertTrue(self.validate_edge_coloring(coloring, graph))


class EulerPartitionTestCase(unittest.TestCase):

  EDGES = [ (0, 3), (3, 0), (0, 4), (4, 0),
            (1, 3), (3, 1), (1, 4), (4, 1), (1, 5), (5, 1),
            (2, 3), (3, 2)]
    
  PARTITION = [[5, 1, 3, 0, 4, 1], 
               [3, 2]]

  SPLIT = ([[4], [3], [], [1], [0], []], 
           [[3], [5, 4], [3], [0, 2], [1], [1]])
  
  def validate_split(self):
    pass

  def validate_partition(self):
    pass
    
  def test_euler_partition_simple(self):
    graph = bgraphs.graph.UDGraph(edges=self.EDGES)
    ep = bgraphs.tools.euler_partition(graph)
    self.assertListEqual(ep, self.PARTITION)

  def test_euler_split_simple(self):
    graph = bgraphs.graph.UDGraph(edges=self.EDGES)
    g1, g2 = bgraphs.tools.euler_split(graph)
    self.assertListEqual(g1.edges, self.SPLIT[0])
    self.assertListEqual(g2.edges, self.SPLIT[1])

if __name__ == '__main__':

  unittest.main()
