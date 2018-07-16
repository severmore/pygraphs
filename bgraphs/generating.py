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

    self.mask_center = (math.floor(r_allowed / self.cell[0]), 
                        math.floor(r_allowed / self.cell[1]))

    self.mask_size = (2 * self.mask_center[0] + 1,
                      2 * self.mask_center[1] + 1)

    self.mask = self.find_mask()
    self.scene = [ [0 
        for _ in range(self.grid[0]) ] 
        for _ in range(self.grid[1]) ]
    
    self._places = list()
    self._available = set()
  

  # TODO proceed case area < r_allowed
  def __call__(self, vertices_num):
    
    if self.r_allowed < self.r_disable or \
       self.area[0] ** 2 < self.r_disable or \
       self.area[1] ** 2 < self.r_disable:
      return None

    return self.generate(vertices_num)
  

  def generate(self, vertices_num):
    """ Generate in the loop a random position among available ones and apply 
    the mask to each position. """

    self._available = set()
    
    init_place = (random.randint(0, self.grid[0] - 1), 
                  random.randint(0, self.grid[1] - 1))
    self._places = [init_place]

    self._apply_mask(init_place)

    for _ in range(1, vertices_num):

      place = self.random_choice(self._available)
      self._places.append(place)
      self._apply_mask(place)
    
    return self._available

  
  def random_choice(self, seq):
    """ Returns a random element from the sequence. """
    i_choice = random.randint(0, len(seq) - 1)
    
    for i, place in enumerate(seq):
      if i == i_choice:
        return place
    
    return None

  
  def _apply_mask(self, place):
    """ Apply mask to the scene with proper positioning to the scene and update 
    available places. """
    # The rules by which scene values are changed when mask is applied.
    MASK = [[0, 1, 2],
            [1, 1, 2],
            [2, 2, 2]]
    
    # The posisition of the left up angle of the mask on the scene.
    mask_pos = (place[0] - self.mask_center[0], 
                place[1] - self.mask_center[1])
    
    # Computes the bounds of iteration loops in which mask is applied if it 
    # isn't placed intirely in the scene.
    mask_start = (0 if mask_pos[0] > 0 else - mask_pos[0], 
                  0 if mask_pos[1] > 0 else - mask_pos[1])

    mask_end = (
        self.grid[0] - mask_pos[0]
          if mask_pos[0] + mask_pos[0] > self.grid[0] 
          else self.mask_size[0],

        self.grid[1] - mask_pos[1]
          if mask_pos[1] + self.mask_size[1] > self.grid[1] 
          else self. mask_size[1]
    )

    for x in range(mask_start[0], mask_end[0]):
      for y in range(mask_start[1], mask_end[1]):

        shift = (x + mask_pos[0], 
                 y + mask_pos[1])

        old = self.scene[shift[0]][shift[1]]

        self.scene[shift[0]][shift[1]] = \
            MASK[ self.scene[shift[0]][shift[1]] ][ self.mask[x][y]]
        
        if old == 1 and self.scene[shift[0]][shift[1]] == 2:
          self._available.remove(shift)
        
        if self.scene[shift[0]][shift[1]] == 1:
          self._available.add(shift)


  def distance(self, i, j):
    """ Returns distance between two points. """
    return ((i[0] - j[0]) * self.cell[0]) ** 2 + \
           ((i[1] - j[1]) * self.cell[1]) ** 2

  
  def find_mask(self):
    """ Returns computed mask. """
    return [ [ self._classify_cell (i, j)
        for j in range(self.mask_size[1]) ] 
        for i in range(self.mask_size[0]) ]


  def _classify_cell(self, i, j):
    """ Classify cell to set of disable (2), available (1) and neutral (0). """
    distance = self.distance((i, j), self.mask_center)
    
    if distance <= self.r_disable:
      return 2
    elif distance <= self.r_allowed:
      return 1
    else:
      return 0 

  
  def is_valid(self):
    """ Returns true if places are valid, i.e. the distance between any two 
    places is greater than disable radius. """
    return not any(
        self.distance(i, j) < self.r_disable
        for i in self._places 
        for j in self._places 
        if i != j)


  def show(self, name):
    """ Display area: mask or scene. """

    area = self.scene if name == 'scene' else \
           self.mask  if name == 'mask'  else [[]]
    
    for pos in self._places:
      area[pos[0]][pos[1]] = '*'
    
    x_coords = "".join([ f'{i % 10:2}' for i in range(len(area)) ])
    separator = '+' + '-' * (len(area) * 2 + 1)
    indent = ' ' * len(name)

    print(f'\n{name}:  {x_coords}')
    print(f'{indent} {separator}')

    for i, line in enumerate(area):

      y_coords = f'{i % 10}|'

      line_str = ' '.join(map(str, line))

      print(indent, y_coords, line_str)

    print()

    for pos in self._places:
      area[pos[0]][pos[1]] = 2


if __name__ == '__main__':
  gen = Geo(100, 200, (800, 800), (25,25))
  gen(5)

  gen.show('scene')
  print('Valid?', gen.is_valid())
