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

  return G1, G2


if __name__ == '__main__':
  
  import bgraphs.graph

  edges = [ (0, 3), (3, 0), (0, 4), (4, 0),
            (1, 3), (3, 1), (1, 4), (4, 1), (1, 5), (5, 1),
            (2, 3), (3, 2)]
  graph = bgraphs.graph.UDGraph(edges=edges)

  print(graph)
  ep = euler_partition(graph)
  print(ep)

  g1, g2 = euler_split(bgraphs.graph.UDGraph(edges=edges))

  print(g1, g2)

