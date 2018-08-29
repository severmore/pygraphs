from collections import deque, Iterable

import bipartite.graph

class SpanningBGraph:
  """ A functor class that finds a spanning bipartite subgraph. """

  METRICS_MAX  = 1000
  METRICS_NONE = 1111

  def __init__(self, graph):
    """ 
    Initialize a class by a graph where to find a spanning bipartite subgraph is
    required.

    Agrs:
      graph(:obj:`UDGraph`) - an undirected graph for which a spanning bipartite
          is to find.
    
    Note:
      Here belonging to different parts of a bipartite graph reffered to as 
      coloring. Giving an initial graph it is sufficient only to store vertex
      coloring.
    """
    self.graph = graph
    self._visited = dict() # a mapping storing pairs coloring - distance
    self._optimum = list()
    self._min_metrics = SpanningBGraph.METRICS_MAX
    self._min_coloring = None
    self._bgraph = None
  

  def __call__(self, init_coloring, max_distance, metrics='regular'):
    """
    Finds a spanning bipartite subgraph of the given graph. To distinguish 
    multiple subgraphs the algorithm uses a metrics. It also start with an
    initial coloring and modify it regarding to `metrics`. 
    
    While operating the algorithm traverses a metagraph; each vertices of it is
    different coloring, that unambiguously corresponds to proper bipartite 
    subgraph knowing an initial graph, and edges connencts the vertices with
    coloring differs by exactly one element.

    So the first algorithm evaluates the subgraph that differs by the color of 
    one vertex, then - by two, etc. As it can require much of memory and time, 
    a parameter `max_distance` is presented that restricts the maximum amount of
     vertices for which color is switched to the other.

    Args:
      init_coloring (:obj:`tuple` of int) - an initial coloring of vertices

      max_distance (int) - specifies how much vertices of an initial coloring
          can be changed
        
      metrics (str) - a metrics regarding which the algorihtm finds a spanning
          bipartite subgraph. Default to 'regular'.
    
    Returns:
      :obj:list of :obj:list of int, float - a list of pairs coloring - min
          metrics. The index of the list is a distance on which this minimal 
          coloring is found.
    
    Note:
      For now different `metrics` is not supported and the only choice is
      'regular'.
    """
    
    if self.graph.edges: 
      is_valid_coloring = (isinstance(init_coloring, Iterable) and
                          len(init_coloring) == self.graph.vertices_num )
      
      if is_valid_coloring and max_distance >= 0:
        
        self.__find(init_coloring, max_distance)
        return self.make_bgraph()
    
    return

  
  def __find(self, init_coloring, max_distance):
    """ 
    Finds an optimal spanning bipartite graph regarding to metrics that
    evaluates how much a subgraph differs from a regular one.
    """

    init_metrics = self.__evaluate_metrics(init_coloring)
    self._optimum = [ (init_coloring, init_metrics) ]
    self._visited[init_coloring] = 0

    distance = 0
    min_coloring = None
    min_metrics  = SpanningBGraph.METRICS_NONE

    queue = deque()
    queue.append(init_coloring)

    while queue:
      
      coloring = queue.popleft()

      if self._visited[coloring] > distance:

        self._optimum.append((min_coloring, min_metrics))
        
        min_coloring = None
        min_metrics  = SpanningBGraph.METRICS_NONE

        distance += 1
        if distance > max_distance:
          break
      
      for vertex in self.graph.get_vertices():
        
        child_coloring = self.__invert_vertex_color(vertex, coloring)

        if child_coloring not in self._visited:
          
          queue.append(child_coloring)
          child_metrics = self.__evaluate_metrics(child_coloring)
          self._visited[child_coloring] = self._visited[coloring] + 1

          if child_metrics < min_metrics:
            min_metrics = child_metrics
            min_coloring = child_coloring
    
    return
      

  def __invert_vertex_color(self, vertex, coloring):
    """ Returns coloring that differs by `vertex` from the given one. """
    vertex_inverted = 0 if coloring[vertex] else 1
    return coloring[:vertex] + (vertex_inverted,) + coloring[vertex+1:]


  def __evaluate_metrics(self, coloring):
    """ Evaluates metrics for the coloring given. """

    degree_max = 0
    degree_sum = 0

    for v in self.graph.get_vertices():
      
      degree_v = 0
      
      for u in self.graph.edges[v]:
        if coloring[v] != coloring[u]:
          degree_v += 1
      
      degree_sum += degree_v

      if degree_v > degree_max:
        degree_max = degree_v

    return self.__metrics(degree_max, degree_sum)
              

  def __metrics(self, degree_max, degree_sum):
    """ Computes metrics of a bipartite graph"""
    if degree_sum:
      return degree_max - degree_sum / self.graph.vertices_num

    return SpanningBGraph.METRICS_MAX
  

  def make_bgraph(self, how='minimum', distance=0):
    """ Return a spanning bipartite graph buiodl from the given vertices 
    coloring and an initial graph via deleting unconsistent edges, i.e. edges
    that connects vertices of the same color. The mehtod is assumed a spanning
    bgraph be found; otherwise returns None.
    
    Args:
      how (str) - takes to value - 'minimum' and 'distance'. If 'minimum' is 
          chosen the method finds the coloring corresponding to the minimum
          value of the metrics; if 'distance' is chosen it finds an optimum
          value on the `distance` specified, i.e. the coloring differs exactly 
          by `distance` colors.
      
      distance (int) - specifies how much colors the initial coloring differs 
          from a local optimum values. It is used when how specified as 
          'distance', otherwise ignored.
    
    Returns:
      :obj:`UDGraph` - the bipartite graph built from the binary coloring and
          a complete graph in which a subgraph is found, if any and `how` is
          correctly specified
      
      None - if a spanning subgraph is not found yet or a parameter `how` 
          specified erroneously.
    """
    if not self._optimum:
      return None

    self._min_metrics = SpanningBGraph.METRICS_MAX
    self._min_coloring = None

    if how == 'minimum':
      
      for col, metrics in self._optimum:
        if metrics < self._min_metrics:
          self._min_metrics = metrics
          self._min_coloring = col
    
    elif how == 'distance':
      
      self._min_coloring = self._optimum[distance][0]
      self._min_metrics  = self._optimum[distance][1]
    
    else:
      return

    self._bgraph = bipartite.graph.UDGraph(
      edges=[ (i, j) for i in self.graph.get_vertices() 
                     for j in range(i + 1, self.graph.vertices_num)
                     if self._min_coloring[i] != self._min_coloring[j] ]
    )

    return self._bgraph


  @staticmethod
  def to_str(coloring):
    return "".join(map(str, coloring))
  

  def reindex(self):
    """ 
    Perform permutation of vertices indexes so that all the vertices of one
    part of a bipartite graph comes first and, after them, the others. 
    """
    if self._min_coloring is None:
      return None

    permutations = [0 for _ in self._min_coloring]
    counter = 0

    for i, color in enumerate(self._min_coloring):
      if color == 1:
        permutations[i] = counter
        counter += 1
    
    for i, color in enumerate(self._min_coloring):
      if color == 0:
        permutations[i] = counter
        counter += 1

    return bipartite.graph.UDGraph(
        edges=[ (permutations[i], permutations[j]) 
            for i in self.graph.get_vertices() 
            for j in range(i + 1, self.graph.vertices_num)
            if self._min_coloring[i] != self._min_coloring[j] ]
        )


  @staticmethod
  def is_bipartite(bgraphs, get_parts=False):

    if not bgraphs or not bgraphs.edges:
      return None
    
    one, two = {0}, set(bgraphs.edges[0])

    completed = {0}

  
    def __fill_parts(active, passive, incidence):

      new_list = list()

      for i in incidence:
        if i not in completed:
          completed.add(i)
          new_list.extend(bgraphs.edges[i])
          active |= set(bgraphs.edges[i])
      
      if len(completed) == bgraphs.vertices_num:
        return

      __fill_parts(passive, active, new_list)
    

    __fill_parts(one, two, bgraphs.edges[0])

    # TODO: Check if conencted

    return one.isdisjoint(two)


   
if __name__ == '__main__':
  import bipartite.generating

  size = 3
  graph = bipartite.generating.grid(size)
  spanning = SpanningBGraph(graph)

  spanning( tuple(0 for _ in range(size ** 2)), size ** 2)

  for i, item in enumerate(spanning._optimum):
    print(f'{i:2} ({SpanningBGraph.to_str(item[0]) }) {item[1]:.4f}')

  print(f'({spanning.to_str(spanning._min_coloring)}) {spanning._min_metrics}')
  print(spanning._bgraph)

  bgraph_con = spanning.reindex()

  print(bgraph_con)

  print('is bipartite?', spanning.is_bipartite(spanning._bgraph))
  print('is bipartite 2?', spanning.is_bipartite(bgraph_con))
  print('graph is bipartite?', spanning.is_bipartite(spanning.graph))



#  class __Node:
#   """ 
#   A containter for alorithm that find a spanning bipartite graph. Not in use
#   for now.
#   """

#   def __init__(self, metrics, degree_max, degree_sum, distance):

#     self.metrics    = metrics    
#     self.degree_max = degree_max 
#     self.degree_sum = degree_sum
#     self.distance   = distance

#   def __str__(self):
#     return (f'node(mu={self.metrics:.4f}, max={self.degree_max}, sum='
#             f'{self.degree_sum}, rho={self.distance})')


#  def __evaluate_coloring(self, vertex, coloring, parent):

#     degree_max = parent.degree_max
#     degree_sum = 0
#     degree_v = 0

#     for u in self.graph.edges[vertex]:

#       if coloring[vertex] == coloring[u]:
#         degree_sum -= 2
      
#       else:
#         degree_sum += 2
#         degree_v += 1
#         degree_u = 0

#         for w in self.graph.edges[u]:
#           if coloring[w] != coloring[u]:
#             degree_u += 1
          
#         if degree_u > degree_max:
#           degree_max = degree_u
    
#     degree_sum += parent.degree_sum
#     if degree_v > degree_max:
#       degree_max = degree_v

#     return self.__Node(
#               self.metrics(degree_max, degree_sum), 
#               degree_max, 
#               degree_sum, 
#               parent.distance + 1)
