# run from terminal as "python christmas-trees.py < test00.in"

import sys

def pretty_print(M):
    for i in range(len(M)):
        for j in range(len(M[0])):
            print(str(M[i][j] if M[i][j] != None else "N").ljust(3, " "),end="")
        print()

n, m = [int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')]
print(n, m)

total_nodes = n * m + n + m + 2
am = [[None for _ in range(total_nodes)] for _ in range(total_nodes)]

# diagonal
for i in range(total_nodes):
    am[i][i] = 0

# first row and column
for i in range(total_nodes):
    if i > 0 and i < (n*m+1):
        am[0][i] = 1
        am[i][0] = 1
    else:
        am[0][i] = 0
        am[i][0] = 0

# last row and column
for i in range(total_nodes):
    if i > (n*m) and i < total_nodes-1:
        am[total_nodes-1][i] = 1
        am[i][total_nodes-1] = 1
    else:
        am[total_nodes - 1][i] = 0
        am[i][total_nodes - 1] = 0

#
for i in range(1, (n*m+1)):
    for j in range(1, (n*m+1)):
        am[i][j] = 0
        am[total_nodes-i-1][total_nodes-j-1] = 0

pretty_print(am)

# for _ in range(n):
#     line = [int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')]
#     print(line)



# example
# T E
# E T

expected = [
    #S N1 N2 N3 N4 R1 R2 C1 C2  T
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0]
]

#   0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
# 0 0 1 1 1 1 1 1 1 1 0 0  0  0  0  0  0
# 1 1 0 0 0 0 0 0 0 0 1 0  1  0  0  0  0
# 2 1
# 3 1
# 4 1
# 5 1
# 6 1
# 7 1
# 8 1
# 9 0
#10 0
#11 0
#12 0
#13 0
#14 0
#15 0

# from wiki
import collections

# This class represents a directed graph using adjacency matrix representation
class Graph:
    def __init__(self, graph):
        self.graph = graph  # residual graph
        self.ROW = len(graph)

    def bfs(self, s, t, parent):
        """Returns true if there is a path from source 's' to sink 't' in
        residual graph. Also fills parent[] to store the path """

        # Mark all the vertices as not visited
        visited = [False] * (self.ROW)

        # Create a queue for BFS
        queue = collections.deque()

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS loop
        while queue:
            u = queue.popleft()

            # Get all adjacent vertices's of the dequeued vertex u
            # If an adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if (visited[ind] == False) and (val > 0):
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        # If we reached sink in BFS starting from source, then return
        # true, else false
        return visited[t]

    # Returns the maximum flow from s to t in the given graph
    def edmonds_karp(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1] * (self.ROW)

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.bfs(source, sink, parent):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow
