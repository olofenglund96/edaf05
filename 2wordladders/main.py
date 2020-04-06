import sys

def parse_input(infile='./data/secret/1small1.in'):
  """
  Parse input and create graph
  """
  if sys.stdin.isatty():
    with open(infile, 'r+') as f:
      file_lines = f.readlines()
      lines = [ l.strip() for l in file_lines ]
  else:
    lines = [ l.strip() for l in sys.stdin ]

  N, Q = [int(l) for l in lines[0].split(" ")]
  del lines[0]

  # create dict of nodes where each key has as array of connected nodes
  nodes = {}
  for i in range(N):
    word = lines[i]
    nodes[word] = []

    for j in range(N):
      if i == j:
        continue

      chars = word[-4:]
      refword = lines[j]
      temp_word = refword
      connected_node = True

      for char in chars:

        if char not in temp_word:
          connected_node = False
          break
        else:
          c_index = temp_word.find(char)

          temp_word = temp_word[0:c_index] + temp_word[c_index+1:]

      if connected_node:
        nodes[word].append(refword)

  # create an array of tuples for each route queried
  routes = []
  for i in range(N,N+Q):
    routes.append(tuple(lines[i].split(" ")))

  return nodes, routes

def find_shortest_path(nodes, route):
  dist = 0
  s, t = route
  q = [s]
  visited = { key: False for key in nodes.keys() }
  visited[s] = True

  while len(q) > 0:
    v = q.pop(0)

    for w in nodes[v]:
      if not visited[w]:
        visited[w] = True
        q.append(w)

        if w == t:
          print(dist)
          return

    dist += 1

  print('Impossible')

def print_graph(nodes, routes):
  import networkx as nx
  import matplotlib.pyplot as plt
  G = nx.Graph()

  for node, edges in nodes.items():
    G.add_node(node)

    for edge_node in edges:
      G.add_edge(node, edge_node)

  plt.figure()
  nx.draw(G, with_labels=True, font_weight='bold')

  plt.savefig('graph.png')

if __name__ == '__main__':
  nodes, routes = parse_input()

  for route in routes:
    find_shortest_path(nodes, route)
