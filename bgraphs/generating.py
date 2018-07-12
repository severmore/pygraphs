"""
Created by Ivanov Roman and Maxim Dudin. This module contains random graph
generators.

https://github.com/severmore/pygraphs
"""

import bgraphs.graph
import random

def bgraph(vertices_num, vratio_low=0.2, vratio_high=0.8, edge_prob=0.5):
    """
    Generates a random bipartite graph. 
    
    Args:
      vertices_num (int) - a number of graph vertices.
    
    Keyword args:
      vratio_low (float) - a lower bound of uniform distribution for a ratio of
          the number of part one and part two of vertices of a bipartite graph.
          Default to 0.2.

      vratio_high (float) - the same as `vratio_low`, but specifies upper bound.

      edge_prob (float) - a floating number from an interval [0,1] - an edge 
          probability.

    Return:
      :obj:'Graph' - a generated graph.
    
    """

    # We apply the rule that part one of vertices is stored in the first
    # portion of the list, and part two - in the second.

    edges = list()
    part_one = round(random.uniform(vratio_low, vratio_high) * vertices_num)

    for start in range(part_one):
      for end in range(part_one, vertices_num):
        
        if random.random() < edge_prob and (start, end) not in edges:
          
          edges.append((start, end))
          edges.append((end, start))
    
    return bgraphs.graph.Graph(edges=edges)


def cycle(vertices_num):
  """
  Generates an undirected cycle with vertices number specified. 
  
  Args:
    vertices_num (int) - a number of vertices in the cycle.

  Return:
    :obj:'UDGraph' - a generated graph.
  
  """
  edges = [ (v, v + 1) for v in range(vertices_num - 1) ]
  edges.append( [(vertices_num - 1), 0] )

  return bgraphs.graph.UDGraph(edges=edges)


def grid(size):
  """
  Generates an undirected graph each vertices forms a quadratic grid for which a 
  number of the vertices on a side is specified, that is exactly 4 vertices has 
  degree 2, (`size` - 2) * 4 vertices has degree 3 and the other (`size` - 2) *
  (`size` - 2) vertices (inner) has degree 4:

            * -- * -- *
            |    |    |
            * -- * -- *
            |    |    |
            * -- * -- *
  
  Args:
    size (int): a number of vertices in the cycle.

  Return:
    :obj:'UDGraph' - a generated graph.
  
  """
  v_num = size ** 2

  horizontal = [ (i, i + 1)    for i in range(v_num) if  (i + 1) % size != 0]
  vertical   = [ (i, i + size) for i in range(v_num) if  i + size < v_num   ]

  return bgraphs.graph.UDGraph(edges=horizontal + vertical)
