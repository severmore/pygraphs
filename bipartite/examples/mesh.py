import random

import bipartite.generating
import bipartite.coloring
import bipartite.graph
import bipartite.spanning

if __name__ == '__main__':

  vertices_num = 10  

  gen = bipartite.generating.Geo(100, 200, (800, 800), (25,25))
  graph = gen(vertices_num)

  gen.show('scene')
  print('Valid?', gen.is_valid())
  print('edges', gen._edges)
  print('initial', graph)

  spanning = bipartite.spanning.SpanningBGraph(graph)
  init_coloring = tuple(random.choices([0,1], k=vertices_num))
  bgraph = spanning(init_coloring, vertices_num)
  bgraph_con = spanning.reindex()

  print('bipartite', bgraph)
  print(bgraph_con)
  print('is bipartite?', spanning.is_bipartite(bgraph))
  print('is bipartite?', spanning.is_bipartite(bgraph_con))
  print('min', spanning._min_coloring)

  coloring = bipartite.coloring.colorize(bgraph)
  coloring_con = bipartite.coloring.colorize(bgraph_con)

  # print(coloring)
  # print(coloring_con)
  print('Vising is valid?', bipartite.coloring.is_valid(coloring, bgraph))
  # print('is valid?', bipartite.coloring.is_valid(coloring_con, bgraph_con))

  graph_copy = bipartite.graph.UDGraph(graph=bgraph)

  print('coppied', graph_copy)
  ch_coloring = bipartite.coloring.colorize(graph_copy, 
                                            algorithm='Cole-Hopcroft')

  print('Cole-Hopcroft coloring', ch_coloring)

  f_ch_coloring = bipartite.coloring.ColeHopcroftColoring.to_commmon_form(
        ch_coloring)
  
  print('formatted', f_ch_coloring)

  print('Cole-Hopcroft is valid?',bipartite.coloring.is_valid(coloring, bgraph))
