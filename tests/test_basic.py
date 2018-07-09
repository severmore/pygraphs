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
    self.assertEqual(graph, graph_origin)
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
  
  def test_graph_creation_by_representation(self):
    graph_origin = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    graph_restored = bgraphs.graph.Graph()
    graph_restored.edges = eval(repr(graph_origin))
    self.assertTrue(graph_origin == graph_restored)



class UndirectedGraphCreationTest(unittest.TestCase):
  """ Test undirected graph creation """

  EDGES_LIST = [ (0, 1), (0, 3), (1, 2), (2, 0), (2, 3) ]
  INCIDENCE  = [[1, 3, 2], [2, 4, 0], [0, 3, 4, 1], [0, 2], [1, 2]]

  def test_undirected_graph_creation_with_graph_specified(self):
    graph_origin = bgraphs.graph.Graph(edges=self.EDGES_LIST)
    graph = bgraphs.graph.UDGraph(graph=graph_origin, edges=[(4,1), (4,2)])
    self.assertIsNotNone(graph)
    self.assertListEqual(graph.edges, self.INCIDENCE)
    self.assertEqual(graph.max_degree, 4)

  def test_undirected_graph_creation_with_undirected_graph_specified(self):
    graph_origin = bgraphs.graph.UDGraph(edges=self.EDGES_LIST)
    graph = bgraphs.graph.UDGraph(graph=graph_origin, edges=[(4,1), (4,2)])
    graph_ref = bgraphs.graph.UDGraph()
    graph_ref.edges = self.INCIDENCE
    self.assertIsNotNone(graph)
    self.assertEqual(graph, graph_ref)
    self.assertEqual(graph.max_degree, 4)



class RemoveAddEdgesGraphTestCase(unittest.TestCase):
  """ Test addition and removing edges to an arbitrary graph. """

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
  """ Test union of two graphs. """
  
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
  """ Test addition and removing edges to an undirected graph. """

  def setUp(self):
    edges = [ (0, 1), (0, 2), (0, 3), (1, 2), (2, 3) ]
    self.udgraph = bgraphs.graph.UDGraph(edges=edges)

  def test_removing_edge(self):
    edges_ref = [ (0, 2), (0, 3), (1, 2), (2, 3)  ]
    undgraph_ref = bgraphs.graph.UDGraph(edges=edges_ref)
    self.udgraph.remove_edge(0, 1)
    self.assertEqual(self.udgraph, undgraph_ref)

  def test_addition_edge(self):
    edges_ref = [ (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3) ]
    undgraph_ref = bgraphs.graph.UDGraph(edges=edges_ref)
    self.udgraph.add_edge(3, 1)
    self.assertEqual(self.udgraph, undgraph_ref)



def validate_coloring(coloring, graph):
  """ Check if edge coloring is valid. """

  for start, incidents in enumerate(graph.edges):
    colorset = { coloring[start, end] for end in incidents }
    
    if len(colorset) != len(graph.edges[start]):
      return False
  
  return True 



class VisingColoringTestCase(unittest.TestCase): 

  def test_vising_coloring_arbitrary_graph_simple(self):
    EDGES = [(0,2), (0,3), (1,2), (1,3), (2,0), (2,1), (3,0), (3,1)]
    graph = bgraphs.graph.Graph(edges=EDGES)
    coloring = bgraphs.coloring.colorize(graph)
    self.assertTrue(validate_coloring(coloring, graph))

  def test_vising_coloring_undirected_graph_simple(self):
    EDGES = [ (0,2), (0,3), (1,2), (1,3) ]
    graph = bgraphs.graph.UDGraph(edges=EDGES)
    coloring = bgraphs.coloring.colorize(graph)
    self.assertTrue(validate_coloring(coloring, graph))
  
  @unittest.skip('skip for a while')
  def test_vising_coloring_generated(self):
    graph = bgraphs.generating.bgraph(20, vratio_low=.4, vratio_high=.6, 
                                      edge_prob=0.3)
    coloring = bgraphs.coloring.colorize(graph)
    self.assertTrue(validate_coloring(coloring, graph))



class ColeHopcroftColoringTestCase(unittest.TestCase):

  def test_cole_hopcoft_coloring_simple(self):
    EDGES = [(0,2), (0,3), (1,2), (1,3)]
    graph = bgraphs.graph.UDGraph(edges=EDGES)
    coloring = bgraphs.coloring.colorize(graph, algorithm='Cole-Hopcroft')
    self.assertTrue(validate_coloring(coloring, graph))




class EulerPartitionTestCase(unittest.TestCase):

  EDGES = [ (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 3) ]
    
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



class ColeHopcroftMatchingTestCase(unittest.TestCase):

  EDGES = [ (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 3) ]

  SPLIT = ([[4], [3], [], [1], [0], []], 
           [[3], [5, 4], [3], [0, 2], [1], [1]])

  MATCHING = [[4], [3], [], [1], [0], []]

  def get_max_degree_vertices(self, graph):

    return { v for v in graph.get_vertices() 
                  if graph.degree(v) == graph.max_degree }

  def is_matching_covers(self, matching, vertices):
    pass


  def test_covering_partition_simple(self):

    print(self.EDGES)
    g0 = bgraphs.graph.UDGraph(edges=self.EDGES)
    print(self.EDGES)
    max_g0 = self.get_max_degree_vertices(g0)

    g1, g2 = bgraphs.tools._covering_partition(g0)
    max_g1 = self.get_max_degree_vertices(g1)
    max_g2 = self.get_max_degree_vertices(g2)

    self.assertListEqual(g2.edges, self.SPLIT[1])
    self.assertListEqual(g1.edges, self.SPLIT[0])
    self.assertTrue(max_g0.issubset(max_g1))
    self.assertTrue(max_g0.issubset(max_g2))

  def test_covering_matching_simple(self):
    graph = bgraphs.graph.UDGraph(edges=self.EDGES)
    # max_graph = self.get_max_degree_vertices(graph)

    matching, rest = bgraphs.tools.covering_matching(graph)
    print('rest', repr(rest))

    self.assertListEqual(matching.edges, self.MATCHING)



if __name__ == '__main__':

  unittest.main()
