import graphviz
import sys, ast

MIN_COLORS = 3
MAX_COLORS = 9

def get_visgraph(wmax):
  """ Return styled graphviz.Graph """
  visgraph = graphviz.Graph()
  visgraph.node_attr.update(
      shape='circle',
      size='10',
      color='lightblue', 
      style='filled', 
      fontcolor='white'
  )
  visgraph.edge_attr.update(
      colorscheme=f'gnbu{wmax}',
      fontsize='10', color='1',
      fontcolor=f'{wmax}'
  )
  return visgraph


if __name__ == '__main__':

  if len(sys.argv) not in {2,3}:
    print('Usage: python visualization.py <weights> [<colornum>]')
    sys.exit()

  weights = ast.literal_eval(sys.argv[1])

  ws_unique = {w for ends in weights for ws in ends.values() for w in ws}
  wbound = lambda w, low, up: up if w > up else low if w < low else w
  colors = (wbound(max(ws_unique) + 2, MIN_COLORS, MAX_COLORS) 
      if len(sys.argv) == 2 
      else int(sys.argv[2])) + 1
  visgraph = get_visgraph(colors)

  edges = set()
  for start, ends in enumerate(weights):
    for end in ends:
      if (end, start) not in edges:
        edges.add((start, end))

        for w in weights[start][end]:
          visgraph.edge(str(start), str(end), 
              label=str(w), color=str(wbound(w+2, 2, colors)))

  visgraph.view(cleanup=True)

  # f.node('0', color='3', pos='2,4!')
  # f.node('1', color='3', pos='4,4!')
  # f.node('2', color='1', pos='2,2!')
  # f.node('3', color='1', pos='4,2!')
