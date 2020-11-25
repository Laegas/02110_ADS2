# run from terminal as "python wifi.py < testfile.in"

import sys
sys.path.insert(1, './lib')
import networkx as nx

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

    graph = nx.Graph()

    for a in selected_a:
        graph.add_edge('s', 1 + selected_a.index(a), capacity = a[3])

    for g in selected_g:
        graph.add_edge(1 + len(selected_a) + selected_g.index(g), 't', capacity = g[2])

    for pair in pairs:
        graph.add_edge(1 + pair[0], 1 + len(selected_a) + pair[2], capacity = pair[1][3])

    max_flow, _ = nx.maximum_flow(graph, 's', 't')

    print(g_not_in_range, max_flow)

run_cProfile = False

if run_cProfile:
    import cProfile
    sys.stdout = open("Benchmarks.txt", "w+")
    cProfile.run('program()')
    sys.stdout.close()
else:
    program()
