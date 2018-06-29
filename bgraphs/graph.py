"""
Created by Ivanov Roman and Maxim Dudin. This module is intended to define
structure describing graphs in this package.

https://github.com/severmore/pygraphs
"""

class Graph:
  """
  A graph representation used in the algorithms of this package. It is intended
  to use in these algos. The vertices of this graph represented by aconsecutive 
  integer numbers, end the edges -- as a list of incidence.

  Note:
      In this implementation as a list used python list that is actually an 
      array

  Attributes:
      edges (:obj:`list` of :obj:`list` of int): a list of incidences.

  """

  def __init__(self, edges=None, graph=None, vertices_num=0):
    """
    Create a new graph object. If none of arguments are given an empty graph 
    will be created.

    Keyword args:

      edges (:obj:`list` of :obj:`turple` of int, optional): a list of edges 
          each element of which is a tuple of size two: (start - end). Default 
          to None.
    
      graph (:obj:`Graph`, optional): a graph which edges will be copied to a 
          new graph. If `edges` and `graph` are both not None then the edges of 
          a newly created graph will contains both `graph` edges and 'edges'. 
          Default to None.

      vertices_num (int, optional): the intended number of vertices in a graph 
          created. If it is not specified it will be obtained from `edges` and 
          'graph' as a maximum of values of vertex identifiers in these 
          variables. The parameter is used to speed up. Default to 0.
    """

    if not vertices_num:
      # As a set of vertices represented as a consequtive integer number it's
      # sufficient to find the gretest one in the list given
      if edges is not None:
        vertices_num = max(max(edges, key=lambda x: max(x[0], x[1]))) + 1
      
      # In the graph object vertices is already structed into the list
      if graph is not None:
        v_max = len(graph.edges)
        
        if v_max > vertices_num:
          vertices_num = v_max
    
    self.edges = [[] for i in range(vertices_num)]

    if edges is not None:
      for start, end in edges:
        self.edges[start].append(end)

    if graph is not None:
      for start, ends in enumerate(graph.edges):
        self.edges[start].extend(ends)

  def __str__(self):
    return str(self.edges)

  def __repr__(self):
    return str(self.edges)


if __name__ == '__main__':
  print(Graph(edges=[(0,1), (0,2), (0, 3)], graph=Graph(edges=[(2,0), (1,2)])))