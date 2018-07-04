"""
Created by Ivanov Roman and Maxim Dudin. This module contains random graph
generators.

https://github.com/severmore/pygraphs
"""

import bgraphs.graph
import random

def bgraph(vertices_num, vratio_low=0.2, vratio_high=0.8,
                            edge_prob=0.9):
    """
    Generates a random bipartite graph. 
    
    Args:
      vertices_num (int): a number of graph vertices.
    
    Keyword args:
      vratio_low (float): a lower bound of uniform distribution for a ratio of
          the number of part one and part two of vertices of a bipartite graph.
          Default to 0.2.

      vratio_high (float): the same as `vratio_low`, but specifies upper bound.

    Return:
      graph(:obj:'Graph'): a generated graph.
    
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
