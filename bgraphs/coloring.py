"""
Created by Ivanov Roman and Maxim Dudin. This module contains edge coloring
algorithm implementation.

https://github.com/severmore/pygraphs
"""

def colorize(graph, algorithm='Vising'):
  """
  Perform minimal edge coloring on a bipartite graph.

  Args:

    graph(:obj:'Graph'): a graph which edges is to color. The algorithm assumes
        graph to be a bipartite without checking and keeping this property is 
        up to user.
    
    algorithm(:obj:`str`, optinal): the algorithm to use for edge coloring. The
        possible values are as follows: "Vising", "Cole-Hopcroft".
  
  Return:

    :obj:`dict` of (:obj:`turple` of int - int): - the resulting coloring of
        edges of a given graph.
  
  References:

    [1] Harold N. Gabow. Using Euler Partition to Edge Color Bipartite 
    Multigraphs // The International Journal of Computer and Information 
    Sciences, Vol. 5, No. 4, 1976.

    [2] Richard Cole, and John Hopcroft. On Edge Coloring Bipartite Graphs //
    SIAM Journal on Computing, Vol. 11, No. 3, pp. 540-546, 1982.

  """
  if algorithm == 'Vising':
    return VisingColoring(graph)()
  
  elif algorithm == 'Cole-Hopcroft':
    return ColeHopcroftColoring(graph)()
  
  return None


class VisingColoring:

  NOCOLOR = -1

  def __init__(self, graph):

    self.graph = graph

    # All colors need to color a given graph. See Vising's Theorem [1]
    self.all_colors = set(range(graph.max_degree)) 

    self.color = dict()
    for start, incidents in enumerate(graph.edges):
      for end in incidents:
        self.color[start, end] = self.NOCOLOR
  

  def __call__(self):

    return self.colorize()


  def set_color(self, vone, vtwo, color):
    """ Set color of an edge of an undirected graph. """

    self.color[vone, vtwo] = color
    self.color[vtwo, vone] = color


  def get_missing_colors(self, vertex):
    """ Get a set of missing colors for a vertex specified. """

    colors_used = { self.color[vertex, end] for end in self.graph.edges[vertex] }
    return self.all_colors - colors_used


  def get_neighbor(self, vertex, color):
    """ 
    Get an neighboring vertex such that a correspongin edge has color specified. 
    """

    for end in self.graph.edges[vertex]:
      if self.color[vertex, end] == color:
        return end
    
    return None


  def colorize(self):
    """ 
    The method finds an edge coloring of an undirtected graph using Vising's
    algorithm.
    """

    for start, end in self.color.keys():

      if self.color[start, end] != self.NOCOLOR:
        continue

      missing_colorset_start = self.get_missing_colors(start)
      missing_colorset_end   = self.get_missing_colors(end)
      missing_colorset_common = missing_colorset_start.intersection(
          missing_colorset_end)

      if missing_colorset_common:
        missing_color = missing_colorset_common.pop()
        self.set_color(start, end, missing_color)
        continue

      color = missing_colorset_start.pop()
      color_next = missing_colorset_end.pop()
      vertex = end
      vertex_next = self.get_neighbor(vertex, color)

      self.set_color(start, end, color)

      # Building an alternating path.
      while vertex_next:
        
        self.set_color(vertex, vertex_next, color_next)

        vertex = vertex_next
        vertex_next = self.get_neighbor(vertex, color_next)
        
        color, color_next = color_next, color

    return self.color



import bgraphs.tools

class ColeHopcroftColoring:

  def __init__(self, graph):
    self.graph = graph
    self.coloring = list()

  def __call__(self):
    return self.colorize(self.graph)
  
  def colorize(self, graph):

    if graph.max_degree % 2:
      
      if graph.max_degree == 1:
        self.coloring.append(graph)
      
      else:
        matching, rest = bgraphs.tools.covering_matching(graph)
        self.coloring.append(matching)
        self.colorize(rest)
    
    else:

      one, two = bgraphs.tools.euler_split(graph)
      self.colorize(one)
      self.colorize(two)

    return self.coloring



if __name__ == '__main__':
  import bgraphs.graph
  graph = bgraphs.graph.UDGraph(edges=
      [ (0, 3), (0, 4), (1, 3), (1, 4), (1, 5), (2, 3)])

  print(graph)

  coloring = colorize(graph, algorithm='Cole-Hopcroft')

  print(coloring)
