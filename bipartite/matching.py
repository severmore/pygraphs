"""
Created by Ivanov Roman and Maxim Dudin.

https://github.com/severmore/pygraphs
"""
from collections import deque

def euler_partition(graph, sustain_graph=False):
  """ 
  Finds an Euler partition of a graph. An Euler partition is a partition of
  edges of a graph into open and close path, each vertex of odd degree is the 
  end of exactly one open path, and each vertex of even degree is the end of
  no open path [1].

  In this implementation an Euler partition is implemented as a list of paths,
  each path is given as a list of vertices that this path passes. For that
  cases when the edges should be including a modificaiton of the method 
  should be considered.

  After finishing this method all edges of an initial graph will be removed as 
  the algorithm supposes. To avoid this set `sustain_graph` to True.
  
  Args:
    graph(:obj:`Graph`) - a graph for which a partition is to find.

    sustain_graph(bool) - if it is set to True graph edges will be copied (not 
        supported yet).
  
  Return:
    :obj:`list` of :obj:`list` of int: an Euler partition representation that 
    is a list of paths. Each path is given by the list of verteces, skipping 
    passing enges.

  References:
    [1] Harold N. Gabow. Using Euler Partition to Edge Color Bipartite 
    Multigraphs // The International Journal of Computer and Information 
    Sciences, Vol. 5, No. 4, 1976.
  """
  if sustain_graph:
    raise NotImplementedError

  partition = list()

  # Populate Q in reverse order comparing to [1]
  queue = deque()
  
  for vertex in graph.get_vertices():
    if graph.degree(vertex) % 2:
      queue.append(vertex)
    else:
      queue.appendleft(vertex)

  while queue:
    start = queue.pop()

    if graph.degree(start):
      
      path = [start]
      pivot = start

      while graph.degree(pivot):

        pivot_next = graph.edges[pivot][0]

        graph.remove_edge(pivot, pivot_next)
        path.append(pivot_next)

        pivot = pivot_next

      partition.append(path)

      if graph.degree(start):
        queue.appendleft(start)

  return partition


def euler_split(graph):
  """
  Returns an Euler split of a graph. An Euler split is two subgraphs of the
  initial graph such that the set of both subgraphs vertices remains unchanged,
  the edges of the graph is a disjoint union of subgraphs edges and these 
  obtains by alteranatively placing the edges of the paths in the Euler 
  partition of the graph to the subgraphs.

  Args:
    graph(:obj:`Graph`) - a graph for which a matching covering maximum degree
        vertices is need to find.

  Returns:
    :obj:`list` of :obj:`turple` of int - a matching to find as a list of edges.
  
  References:
    [1] Harold N. Gabow. Using Euler Partition to Edge Color Bipartite 
    Multigraphs // The International Journal of Computer and Information 
    Sciences, Vol. 5, No. 4, 1976.
  """

  G1 = graph.__class__(vertices_num=graph.vertices_num)
  G2 = graph.__class__(vertices_num=graph.vertices_num)

  partition = euler_partition(graph)

  for path in partition:
    v_prev, path = path[0], path[1:]

    for index, vertex in enumerate(path):

      if index % 2:
        G1.add_edge(v_prev, vertex)
      else:
        G2.add_edge(v_prev, vertex)

      v_prev = vertex
  
  G1.update_max_degree()
  G2.update_max_degree()

  return G1, G2



def _covering_partition(graph):
  """ 
  Finds Cole-Hopcroft graph partition - a partition into two subgraphs such that
   the following properties holds:
    -  both subgraphs have the same to graph vertices,
    -  a disjoint union of thier edges forms the edges of the initial graph,
    -  the set of vertices having maximum degree in the graph also have maximum
    degree in each subgraphs.

  If the maximum degree of the initial graph is even then Cole-Hopcroft 
  partition is just an Euler split.

  Args:
    graph(:obj:`Graph`) - a graph to split

  Returns:
    :obj:`Graph`, :obj:`Graph` - two subraphs of `graph`.

  References:
    [2] Richard Cole, and John Hopcroft. On Edge Coloring Bipartite Graphs //
    SIAM Journal on Computing, Vol. 11, No. 3, pp. 540-546, 1982.
  """

  if graph.max_degree % 2 == 0:
    return euler_split(graph) 

  D = graph.max_degree

  k, d = D // 4, 1
  
  if D % 4 == 3:
    k, d = k + 1, -1

  # Find M-containing set - a set of max degree vertices in a graph.
  M = { v for v in graph.get_vertices() if graph.degree(v) == D }

  H1, H2 = euler_split(graph)

  # M1 is a subset of M which vertices have degree 2 * k + d in H1. If M1 have 
  # less vertices than half of M then swap H1 and H2, M1 and M2; so M1 should 
  # have at least half of maximum degree vertices.

  M1 = { v for v in M if H1.degree(v) == 2 * k + d }
  M2 = M - M1

  if len(M1) < len(M) / 2:
    H2, H1 = H1, H2
    M2, M1 = M1, M2

  # Iterates till in both the subraphs the set of max degree vertices equals M
  while M2:

    H21, H22 = euler_split(H2)
    
    M21 = { v for v in M2 if H21.degree(v) == k + d }
    M22 = M2 - M21

    if len(M21) < len(M2) / 2:
      H22, H21 = H21, H22
      M22, M21 = M21, M22

    H1.union(H21)
    H2 = H22

    if k % 2:
      k = k / 2
    else:
      H1, H2 = H2, H1 
      k = (D - k) / 2
      d = -d

    M1 = M1.union(M21)
    M2 = M22

  H1.update_max_degree()
  H2.update_max_degree()

  return H1, H2


def covering_matching(graph, sustain_graph=True):
  """ 
  Finds matching covering maximum degree vertices of a graph. The matching is a
  subset of a graph edges such that no two edges have common vertex. It is said
  that matching covers a set of vertices, if for all vertex from this set there
  is an edge from matching that contains this vertex.

  After finishing this method all edges of an initial graph will be removed as 
  the algorithm supposes. If it is necessary to keep graph edges set 
  `sustain_graph` to True, and the method return both matching edges and the 
  rest part of the edges. If one need to recover the initial graph just union
  this edges into a single graph.

  Args:
    graph(:obj:`Graph`) - a graph to split

    sustain_graph(bool) - if it is set to True graph edges excluding the edges
    of matching found will be returned.

  Returns:
    :obj:`list` of :obj:`list` of int, :obj:`Graph` - a matching and the rest of
        `graph` if `sustain_graph` is set to True.

    :obj:`list` of :obj:`list` of int - a matching found if `sustain_graph` 
        is set to False.

  References:
    [2] Richard Cole, and John Hopcroft. On Edge Coloring Bipartite Graphs //
    SIAM Journal on Computing, Vol. 11, No. 3, pp. 540-546, 1982.
  """
  if sustain_graph:

    matching, rest = graph, graph.__class__()

    # The first iteration of cycle is individually coded to avoid superfluous
    # coping of graph edges to `rest`.

    if matching.max_degree > 1:
      matching, rest = _covering_partition(matching)

      if matching.max_degree > rest.max_degree:
        matching, rest = rest, matching

    while matching.max_degree > 1:
      G1, G2 = _covering_partition(matching)

      if G1.max_degree > G2.max_degree:
        G1, G2 = G2, G1

      matching = G1
      rest.union(G2)
      
    return matching, rest
  
  else:

    matching = graph

    while matching.max_degree > 1: 

      G1, G2 = _covering_partition(matching)
      matching = G1 if G1.max_degree < G2.max_degree else G2
    
    return matching



# TODO: add get edges
def weight_redistibution(graph, sustain_graph=False):
  """
  Perform weight redistibution for edges of a regular bipartite graph so that 
  each edge is initially granted zero weight, and at the end for each vertex in 
  the graph only one incident edge has non-zero weigh, being equal to a maximum 
  degree value.

  Args:
    graph(`obj`:`graph`) - a given graph

    sustain_graph(bool) - if it is set to True graph edges will be copied (not 
        supported yet).
  """
  weight = {start : {end : 1 
              for end in incident} 
              for start, incident in graph.edges}
  
  if sustain_graph:
    raise NotImplementedError


  
def reweight(graph, partitions):

  def _reweight(start, end, where):
    graph.remove_edge(start, end)
    partitions[where].add_edge(start, end)
  
  def next_vertex(path):
    head = path[-1]
    if len(path) == 1 or graph.edges[head][0] != path[-2]:
      return graph.edges[head][0]
    return graph.edges[head][1]
  

  for vertex in graph.get_vertices():
    if graph.degree(vertex):

      path = [vertex]

      while path:
        head = path[-1]

        if graph.degree(head) == 0:
          path.pop()
          continue
        
        if graph.degree(head) == 1 and len(path) > 1:
          path.pop()
          _reweight(head, path[-1], 1)
          continue

        v_next = next_vertex(path)
          
        if v_next in path:
          start = v_next
          switcher = 1

          while path[-1] != v_next:
            end = path.pop()
            _reweight(start, end, switcher + 1)
            start = end
            switcher *= -1
          
          _reweight(start, v_next, switcher + 1)

        else:
          path.append(v_next)
        
  return partitions


  



if __name__ == '__main__':

  import bipartite.graph
  import bipartite.generating
  import bipartite.tools

  # graph = bipartite.graph.UDGraph(edges=
  #     [ (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 3)])
  # print('graph: ', graph)

  # euler_partition(graph, sustain_graph=True)

  # matching, rest = covering_matching(graph)
  # print('matching: ', matching)
  # print('rest: ', repr(rest))

  # rest.union(matching)
  # graph = bipartite.graph.UDGraph(edges=
  #     [ (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 3)])
  
  # for i, graph in enumerate(reweight(graph)):
  #   print(f'[{i}] {graph}')

  # print('restored: ', rest)
  # print('equality of rest and graph: ', rest == graph)

  # graph = bipartite.generating.grid(3)

  graph = bipartite.generating.bgraph(10, kind='ugraph')

  print(graph)

  # graph = bipartite.graph.UDGraph(graph=graph)
  graph_ref = bipartite.graph.UDGraph(graph=graph)

  partitions = [bipartite.graph.UDGraph(vertices_num=graph.vertices_num) 
                    for _ in range(3)]
  three_graphs = reweight(graph, partitions)
  # for i, g in enumerate(three_graphs):
  #   print(f'[{i}] {g}')

  print('is acyclic ', bipartite.tools.has_cycle(three_graphs[1]))
  print('is empty ', list(graph.get_edges()))
  
  graph.union(three_graphs[0]).union(three_graphs[1]).union(three_graphs[2])
  print(graph == graph_ref)
  



  

  
   
  
