import bgraphs.graph
from collections import deque, Iterable

class SpanningBGraph:

  class __Node:

    def __init__(self, metrics, degree_max, degree_sum, distance):

      self.metrics    = metrics    
      self.degree_max = degree_max 
      self.degree_sum = degree_sum
      self.distance   = distance

    def __str__(self):
      return (f'node(metrics={self.metrics}, max={self.degree_max}, sum='
              f'{self.degree_sum}, distance={self.distance})')


  METRICS_MAX  = 1000
  METRICS_NONE = METRICS_MAX + 111


  def __init__(self, graph):
    self.graph = graph
    self.visited = dict()
  

  def __call__(self, init_bitgraph, distance):
    
    if self.graph.edges: 
      is_valid_bitgraph = (isinstance(init_bitgraph, Iterable) and
                          len(init_bitgraph) == self.graph.vertices_num )
      
      if is_valid_bitgraph and distance >= 0:
        return self.__find(init_bitgraph, distance)
    
    return None

  
  def __find(self, init_coloring, max_distance):

    init_node = self.__evaluate_init_coloring(init_coloring)

    # print('init', init_coloring, init_node)

    self.visited[init_coloring] = init_node

    distance = 0
    min_coloring = None
    min_metrics  = SpanningBGraph.METRICS_NONE
    optimum_coloring = [ (init_coloring, init_node.metrics) ]

    queue = deque()
    queue.append(init_coloring)

    while queue:
      
      coloring = queue.popleft()

      if self.visited[coloring].distance > distance:

        print(distance, min_coloring, min_metrics)

        optimum_coloring.append((min_coloring, min_metrics))
        
        min_metrics  = SpanningBGraph.METRICS_NONE
        min_coloring = None

        distance += 1
        if distance > max_distance:
          break
    
      # print('Q: ', distance, coloring, queue)

      for vertex in self.graph.get_vertices():
        
        child_coloring = self.__invert_vertex_color(vertex, coloring)

        if child_coloring not in self.visited:
          
          queue.append(child_coloring)
          node = self.visited[coloring]
          child_node = self.__evaluate_coloring(vertex, child_coloring, node)
          self.visited[child_coloring] = child_node

          # print('    - child', child_coloring, child_node)

          # On the same distance
          if child_node.metrics < min_metrics:
            min_metrics = child_node.metrics
            min_coloring = child_coloring
      
    return optimum_coloring


  def __invert_vertex_color(self, vertex, coloring):
    vertex_inverted = 0 if coloring[vertex] else 1
    return coloring[:vertex] + (vertex_inverted,) + coloring[vertex+1:]


  def __evaluate_coloring(self, vertex, coloring, parent):

    degree_max = parent.degree_max
    degree_sum = 0
    degree_v = 0

    for u in self.graph.edges[vertex]:


      if coloring[vertex] == coloring[u]:
        degree_sum -= 2
      
      else:
        degree_sum += 2
        degree_v += 1
        degree_u = 0

        for w in self.graph.edges[u]:
          if coloring[w] != coloring[u]:
            degree_u += 1
          
        if degree_u > degree_max:
          degree_max = degree_u
    
    degree_sum += parent.degree_sum
    if degree_v > degree_max:
      degree_max = degree_v

    return self.__Node(
              self.metrics(degree_max, degree_sum), 
              degree_max, 
              degree_sum, 
              parent.distance + 1)


  def __evaluate_init_coloring(self, bitgraph):

    degree_max = 0
    degree_sum = 0

    for v in self.graph.get_vertices():
      
      degree_v = 0
      
      for u in self.graph.edges[v]:
        if bitgraph[v] != bitgraph[u]:
          degree_v += 1
      
      degree_sum += degree_v

      if degree_v > degree_max:
        degree_max = degree_v

    return self.__Node(
              self.metrics(degree_max, degree_sum), 
              degree_max, 
              degree_sum, 
              0)
  

  def metrics(self, degree_max, degree_sum):
    if degree_sum:
      # print('          ', degree_max, degree_sum, self.graph.vertices_num)
      return degree_max - degree_sum / self.graph.vertices_num
    return SpanningBGraph.METRICS_MAX



def generate_cycle(vertices_num):

  edges = [ (v, v + 1) for v in range(vertices_num - 1) ]
  edges.append( [(vertices_num - 1), 0] )

  return bgraphs.graph.UDGraph(edges=edges)    


if __name__ == '__main__':

  cycle_len = 20

  graph = generate_cycle(cycle_len)

  print(graph)

  spanning = SpanningBGraph(graph)

  print('-'*80)
  result = spanning( tuple(1 for _ in range(cycle_len)),  cycle_len  )
  print('-'*80)
  # for i, item in enumerate(result):
  #   print(i, item)