# run from terminal as "python wifi.py < testfile.in"

import sys
import os
import platform
print(platform.platform())
sys.path.insert(1, '.\lib')

print(sys.platform)
print(os.name)

import thinmaxflow as tf

def program():

    # read the input file
    gn, an, wn = [int(s) for s in sys.stdin.readline().split()]

    g = []
    a = []

    for i in range(gn): # read groups
        g.append([int(s) for s in sys.stdin.readline().split()])

    for i in range(an): # read access points
        a.append([int(s) for s in sys.stdin.readline().split()])

    # ignore walls for mandatory part

    selected_a = []
    selected_g = []
    pairs = []

    g_not_in_range = 0
    for gx in g:
        in_range = False
        for ax in a:
            if ((gx[0] - ax[0])**2+(gx[1] - ax[1])**2)**0.5 <= ax[2]:
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
