# run from terminal as "python wifi.py < testfile.in"

import sys
sys.path.insert(1, '.\lib')

import thinmaxflow as tf

def intersects(a,b,c,d,p,q,r,s):
  det = (c - a) * (s - q) - (r - p) * (d - b);
  if det == 0:
    return False
  else:
    lam = ((s - q) * (r - a) + (p - r) * (s - b)) / det
    gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det
    return (0 < lam < 1) and (0 <= gamma <= 1)

def program():

    # read the input file
    gn, an, wn = [int(s) for s in sys.stdin.readline().split()]

    g = []
    a = []
    w = []

    for i in range(gn): # read groups
        g.append([int(s) for s in sys.stdin.readline().split()])

    for i in range(an): # read access points
        a.append([int(s) for s in sys.stdin.readline().split()])

    for i in range(wn): # read walls
        w.append([int(s) for s in sys.stdin.readline().split()])

    selected_a = []
    selected_g = []
    pairs = []

    g_not_in_range = 0
    for gx in g:
        in_range = False
        for ax in a:
            intersect = False
            if ((gx[0] - ax[0])**2+(gx[1] - ax[1])**2)**0.5 <= ax[2]:
                for wx in w:
                    if intersects(gx[0], gx[1], ax[0], ax[1], wx[0], wx[1], wx[2], wx[3]):
                        intersect = True
                        break
                if not intersect:
                    in_range = True
                    if ax not in selected_a:
                        selected_a.append(ax)
                    if gx not in selected_g:
                        selected_g.append(gx)
                    pairs.append((selected_a.index(ax), ax, selected_g.index(gx), gx))
        if not in_range: g_not_in_range += gx[2]

    graph = tf.GraphInt()

    a_node_first = graph.add_node(len(selected_a))
    g_node_first = graph.add_node(len(selected_g))

    for i, a in enumerate(range(a_node_first, len(selected_a) + a_node_first)):
        graph.add_tweights(a, selected_a[i][3], 0)

    for i, g in enumerate(range(g_node_first, len(selected_g) + g_node_first)):
        graph.add_tweights(g, 0, selected_g[i][2])

    for pair in pairs:
        graph.add_edge(a_node_first + pair[0], g_node_first + pair[2], pair[1][3], 0)

    max_flow = graph.maxflow()

    print(g_not_in_range, max_flow)

run_cProfile = False

if run_cProfile:
    import cProfile
    sys.stdout = open("Benchmarks.txt", "w+")
    cProfile.run('program()')
    sys.stdout.close()
else:
    program()
