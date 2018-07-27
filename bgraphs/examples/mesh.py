import random

import bgraphs.generating
import bgraphs.spanning
import bgraphs.coloring
import bgraphs.graph

if __name__ == '__main__':

  vertices_num = 10  

  gen = bgraphs.generating.Geo(100, 200, (800, 800), (25,25))
  graph = gen(vertices_num)

  gen.show('scene')
  print('Valid?', gen.is_valid())
  print('edges', gen._edges)
  print('initial', graph)

  spanning = bgraphs.spanning.SpanningBGraph(graph)
  init_coloring = tuple(random.choices([0,1], k=vertices_num))
  bgraph = spanning(init_coloring, vertices_num)
  bgraph_con = spanning.reindex()

  print('bipartite', bgraph)
  print(bgraph_con)
  print('is bipartite?', spanning.is_bipartite(bgraph))
  print('is bipartite?', spanning.is_bipartite(bgraph_con))
  print('min', spanning._min_coloring)

  coloring = bgraphs.coloring.colorize(bgraph)
  coloring_con = bgraphs.coloring.colorize(bgraph_con)

  # print(coloring)
  # print(coloring_con)
  print('Vising is valid?', bgraphs.coloring.is_valid(coloring, bgraph))
  # print('is valid?', bgraphs.coloring.is_valid(coloring_con, bgraph_con))

  graph_copy = bgraphs.graph.UDGraph(graph=bgraph)

  print('coppied', graph_copy)
  ch_coloring = bgraphs.coloring.colorize(graph_copy, algorithm='Cole-Hopcroft')

  print('Cole-Hopcroft coloring', ch_coloring)

  f_ch_coloring = bgraphs.coloring.ColeHopcroftColoring.to_commmon_form(
        ch_coloring)
  
  print('formatted', f_ch_coloring)

  print('Cole-Hopcroft is valid?', bgraphs.coloring.is_valid(coloring, bgraph))
