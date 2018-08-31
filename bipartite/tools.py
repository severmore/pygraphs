"""
Created by Ivanov Roman.

https://github.com/severmore/pygraphs
"""
from collections import deque


def dfs(graph, func, start=0):
  """
  Traverse a `graph` using depth-first search and starting with `start`, and 
  apply function `func` to each vertices.
  """
  stack = deque()
  visited = [False for _ in graph.get_vertices()]

  for vertex in graph.get_vertices():
    if not visited[vertex]:
      
      stack.append(vertex)
      visited[vertex] = True
      
      while stack:
        v = stack.pop()
        func(v)

        for destination in graph.edges[v]:
          if not visited[destination]:
            stack.append(destination)
            visited[destination] = True


def dfs2(graph, func, start=0):
  """
  Traverse a `graph` using depth-first search and starting with `start`, and 
  apply function `func` to each vertices. Recursive variant of the algorithm.
  """
  visited = [False for _ in graph.get_vertices()]

  def __recursive(start):
    visited[start] = True
    func(start)

    for destination in graph.edges[start]:
      if not visited[destination]:
        __recursive(destination)

  __recursive(start)


def has_cycle(graph):
  """
  `obj`:`graph` -> bool. Ask whether a graph given has cycle or not, using 
  colors.
  """
  def _has_cycle(vertex):
    # recolor vertex
    whites.remove(vertex)
    grays.add(vertex)

    # visit neighbors
    for neighbor in graph.edges[vertex]:

      # end is already visited, a cycle is found
      if neighbor in grays:
        return True

      # ignore blacks
      if neighbor in blacks:
        continue
      
      # traverse a neighbor recursively
      if _has_cycle(neighbor):
        return True
    
    grays.remove(vertex)
    blacks.add(vertex)
      
  # white - not processed
  # gray  - currently being processed
  # black - comleted
  
  whites = set(graph.get_vertices())
  grays  = set()
  blacks = set()

  # Traverse only whites
  for vertex in graph.get_vertices():
    if vertex in whites and _has_cycle(vertex):
      return True
  
  return False


def has_cycle2(graph):
  """
  `obj`:`graph` -> bool. Ask whether a graph given has cycle or not, recursive 
  implementation.
  """
  visited = [False for _ in graph.get_vertices()]

  def _has_cycle(vertex, parent):
    visited[vertex] = True

    for destination in graph.edges[vertex]:

      if destination != parent and visited[destination]:
        return True

      elif _has_cycle(destination, vertex):
        return True
    
    return False

  for vertex in graph.get_vertices():
    if not visited[vertex] and _has_cycle(vertex, -1):
        return True
  
  return False


def has_cycle3(graph):
  """
  `obj`:`graph` -> bool. Ask whether a graph given has cycle or not, disjoint
  sets implementation.
  """
  parent = list(graph.get_vertices())

  def find(vertex):
    if parent[vertex] != vertex:
      return find(parent[vertex])
    return vertex
  
  def union(one, two):
    parent_one = find(one)
    parent_two = find(two)

    parent[parent_two] = parent_one
  
  for start, end in graph.get_edges():
    set_start = find(start)
    set_end = find(end)

    if set_start == set_end:
      return True
    
    union(set_start, set_end)
  
  return False


if __name__ == '__main__':
  import bipartite.graph

  get_graph = lambda: bipartite.graph.Graph(edges=[
        (0,1), (0,2), (1,2), (1,3), (3,4), (2,3), (4,0), (4,1), (4,5), ])
  
  dfs(get_graph(), print, start=1)

  get_cycle = lambda: bipartite.graph.Graph(edges=[
        (0,1), (1,2), (2,3), (3,4), (4,5)])

  print(has_cycle3(get_cycle()))
