"""
Created by Ivanov Roman and Maxim Dudin. This module contains random graph
generators.

https://github.com/severmore/pygraphs
"""

import bgraphs.graph
import random
import math

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


class Geo:

  def __init__(self, r_disable, r_allowed, area, grid):
    
    self.r_disable = r_disable ** 2
    self.r_allowed = r_allowed ** 2
    self.area = area
    self.grid = grid

    self.cell = (area[0] / grid[0],
                 area[1] / grid[1])

    print('cell', self.cell)
    
    self.mask_center = (math.floor(r_allowed / self.cell[0]), 
                        math.floor(r_allowed / self.cell[1]))
    
    print('center', self.mask_center)

    self.mask_size = (2 * self.mask_center[0] + 1,
                      2 * self.mask_center[1] + 1)
    
    print('size', self.mask_size)

    self.mask = self.find_mask()

    print('mask', self.mask)

    self.scene = [ [0 
        for _ in range(self.grid[0]) ] 
        for _ in range(self.grid[1]) ]
  

  # TODO proceed case area < r_allowed
  def __call__(self, vertices_num):
    
    if self.r_allowed < self.r_disable or \
       self.area[0] ** 2 < self.r_disable or \
       self.area[1] ** 2 < self.r_disable:
      return None

    return self.generate(vertices_num)
  

  def generate(self, vertices_num):

    init_place = (random.randint(0, self.grid[0] -1), 
                random.randint(0, self.grid[1] -1))
    
    places = [init_place]

    print('position', places[0])
    
    places_available = set()

    self.process_place(init_place, places_available)
    self.show(self.scene, 'scene')

    for _ in range(1, vertices_num):
      
      i_place = random.randint(0, len(places_available) - 1)
      pos = 0
      for i, place in enumerate(places_available):
        if i == i_place:
          pos = place
          break
      
      print(pos)
      places.append(pos)

      self.process_place(pos, places_available)
      self.show(self.scene, 'scene')


    for pos in places:
      self.scene[pos[0]][pos[1]] = '*'
    
    self.show(self.scene, 'scene')


    print('Valid?', self.is_valid(places))

    return places_available

  
  def process_place(self, place, places_available):

    mask_shift = (place[0] - self.mask_center[0], 
                  place[1] - self.mask_center[1])

    print('shift', mask_shift)
    
    MASK = [[0, 1, 2],
            [1, 1, 2],
            [2, 2, 2]]
    
    mask_start = (0 if mask_shift[0] > 0 else - mask_shift[0], 
                  0 if mask_shift[1] > 0 else - mask_shift[1])

    mask_end = (
        self.grid[0] - mask_shift[0]
          if mask_shift[0] + mask_shift[0] > self.grid[0] 
          else self.mask_size[0],

        self.grid[1] - mask_shift[1]
          if mask_shift[1] + self.mask_size[1] > self.grid[1] 
          else self. mask_size[1]
    )

    for x in range(mask_start[0], mask_end[0]):
      for y in range(mask_start[1], mask_end[1]):

        shift = (x + mask_shift[0], 
                 y + mask_shift[1])

        old = self.scene[shift[0]][shift[1]]

        self.scene[shift[0]][shift[1]] = \
            MASK[ self.scene[shift[0]][shift[1]] ][ self.mask[x][y]]
        
        if old == 1 and self.scene[shift[0]][shift[1]] == 2:
          places_available.remove(shift)
        
        if self.scene[shift[0]][shift[1]] == 1:
          places_available.add(shift)


  def distance(self, i, j):
    """ Returns distance between two points. """
    return ((i[0] - j[0]) * self.cell[0]) ** 2 + \
           ((i[1] - j[1]) * self.cell[1]) ** 2

  
  def find_mask(self):
    """ Returns computed mask. """
    mask = [ [0 
        for _ in range(self.mask_size[1]) ] 
        for _ in range(self.mask_size[0]) ]

    for x in range(self.mask_size[0]):
      for y in range(self.mask_size[1]):

        distance = self.distance((x,y), self.mask_center)

        if distance <= self.r_disable:
          mask[x][y] = 2
        
        elif distance <= self.r_allowed:
          mask[x][y] = 1
    
    return mask

  
  def is_valid(self, places):

    print('positions', places)
    print('disable', self.r_disable)

    return not any(
        self.distance(i, j) < self.r_disable
        for i in places 
        for j in places 
        if i != j)


  def show(self, area, name):

    coord_horizontal = "".join([ f'{i % 10:2}' for i in range(len(area)) ])
    sep_horizontal = '+' + '-' * (len(area) * 2 + 1)
    indent = ' ' * len(name)

    print(f'\n{name}:  {coord_horizontal}')
    print(f'{indent} {sep_horizontal}')

    for i, line in enumerate(area):

      coord_vertical = f'{i % 10}|'

      line_str = ' '.join(map(str, line))

      print(indent, coord_vertical, line_str)

    print()


if __name__ == '__main__':
  # geo(5, 100, 200, (800, 800), (25,25))
  gen = Geo(100, 200, (800, 800), (25,25))
  gen(5)
