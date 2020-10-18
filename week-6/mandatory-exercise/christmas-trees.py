# run from terminal as "python christmas-trees.py < testfile.in"

import sys
import collections

# read the input file
n, m = [int(s) for s in sys.stdin.readline().split()]
trees_matrix = [[None for _ in range(m)] for _ in range(n)]

for i in range(n):
    line = [int(s) for s in sys.stdin.readline().split()]
    for j in range(1, len(line)):
        trees_matrix[i][line[j]] = 1

# define graph classes
class FlowEdge:
    def __init__(self, v, w, capacity):
        self.from_vertex = v
        self.to_vertex = w
        self.capacity = capacity
        self.flow = 0

    def other(self, vertex):
        if vertex == self.from_vertex:
            return self.to_vertex
        elif vertex == self.to_vertex:
            return self.from_vertex
        else:
            raise Exception("Error")

    def residual_capacity_to(self, vertex):
        if vertex == self.from_vertex:
            return self.flow
        elif vertex == self.to_vertex:
            return self.capacity - self.flow
        else:
            raise Exception("Error")

    def add_residual_flow_to(self, vertex, flow_to_add):
        if vertex == self.from_vertex:
            self.flow -= flow_to_add
        elif vertex == self.to_vertex:
            self.flow += flow_to_add
        else:
            raise Exception("Error")

    def __str__(self):
        return "From " + str(self.from_vertex) + " to " + str(self.to_vertex) + "; cap: " + str(self.capacity) + "; flow: " + str(self.flow)

class FlowGraph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.edgeTo = None
        self.E = 0

    def add_edge(self, e: FlowEdge):
        self.adj[e.from_vertex].append(e)
        self.adj[e.to_vertex].append(e)
        self.E += 1

    def has_augmenting_path_bfs(self):
        self.edgeTo = [None for _ in range(self.V)]
        visited = set()
        queue = collections.deque([0])  # source s = 0
        visited.add(0)

        while queue:
            v = queue.popleft()
            for e in self.adj[v]:
                w = e.other(v)
                if w not in visited and e.residual_capacity_to(w) > 0:
                    self.edgeTo[w] = e
                    if w == self.V - 1:
                        return True
                    visited.add(w)
                    queue.append(w)
        return False

    def has_augmenting_path_dfs(self, start=0, visited=None):
        if visited is None:
            self.edgeTo = [None for _ in range(self.V)]
            visited = set()
        visited.add(start)

        for e in self.adj[start]:
            if self.V - 1 in visited:
                return True
            w = e.other(start)
            if w not in visited and e.residual_capacity_to(w) > 0:
                self.edgeTo[w] = e
                self.has_augmenting_path_dfs(w, visited)

        return self.V - 1 in visited

    def ford_fulkerson(self):
        total_flow = 0
        while self.has_augmenting_path_dfs():  # calculates edgeTo
            # initialize some big bottleneck
            bottleneck = 1000

            # calculate the actual bottleneck
            current = self.V - 1  # start from sink t
            while current != 0:  # until source s
                bottleneck = min(bottleneck, self.edgeTo[current].residual_capacity_to(current))
                current = self.edgeTo[current].other(current)

            # augment the path with the bottleneck
            current = self.V - 1  # start from sink t
            while current != 0:  # until source s
                self.edgeTo[current].add_residual_flow_to(current, bottleneck)
                current = self.edgeTo[current].other(current)

            total_flow += bottleneck
        return total_flow

# Create graph and edges
total_vertices = n + m + 2
graph = FlowGraph(total_vertices)
debug_graph_building = False

# add edges from source to the row vertices with capacity of two
for i in range(1, n + 1):
    from_to = [0, i]
    if debug_graph_building: print(from_to, 2)
    graph.add_edge(FlowEdge(from_to[0], from_to[1], 2))

# add appropriate edges from row to the column vertices
for i in range(n):
    for j in range(m):
        if trees_matrix[i][j] is None:
            from_to = [1 + i, 1 + n + j]
            if debug_graph_building: print(from_to)
            graph.add_edge(FlowEdge(from_to[0], from_to[1], 1))

# add edges from column vertices to sink t = total_vertices - 1
for i in range(total_vertices - m - 1, total_vertices - 1):
    from_to = [i, total_vertices - 1]
    if debug_graph_building: print(from_to)
    graph.add_edge(FlowEdge(from_to[0], from_to[1], 1))

run_cProfile = False

if run_cProfile:
    import cProfile
    sys.stdout = open("Benchmarks.txt", "w+")
    cProfile.run('graph.ford_fulkerson()')
    sys.stdout.close()
else:
    print(graph.ford_fulkerson())
