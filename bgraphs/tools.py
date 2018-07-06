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

    sustain_graph(bool) - if it is set to True graph edges will be copied.
  
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
    pass

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
    graph(:obj:`Graph`) - a graph to split

  Returns:
    graph(:obj:`Graph`), graph(:obj:`Graph`) - two subraphs of `graph`.
  
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


def find_covering_matching(graph):
  pass


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
    graph(:obj:`Graph`), graph(:obj:`Graph`) - two subraphs of `graph`.

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

  # Iterates till in both subraphs the set of max degree vertices equals M
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


if __name__ == '__main__':

  import bgraphs.graph

  EDGES = [ (0, 3), (3, 0), (0, 4), (4, 0),
          (1, 3), (3, 1), (1, 4), (4, 1), (1, 5), (5, 1),
          (2, 3), (3, 2)]
  
  graph = bgraphs.graph.UDGraph(edges=EDGES)
  print(graph)
  g1, g2 = _covering_partition(graph)

  print(g1)
  print(g2)
