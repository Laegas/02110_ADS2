# run from terminal as "python christmas-trees.py < test00.in"

import sys
import collections

# read the input file
n, m = [int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')]
empty_squares = 0
trees_matrix = [[None for _ in range(m)] for _ in range(n)]

for i in range(n):
    line = [int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')]
    empty_squares += m - line[0]
    for j in range(1, len(line)):
        trees_matrix[i][line[j]] = 1

# def pretty_print(M):
#     for i in range(len(M)):
#         for j in range(len(M[0])):
#             print(str(M[i][j] if M[i][j] != None else "N").ljust(3, " "),end="")
#         print()

# class FlowEdge:
#     def __init__(self, value, cap):
#         self.vertex = value
#         self.next = None
#         self.cap = cap
#         self.flow = 0
#
#     def __str__(self):
#         return "Vertex " + str(self.vertex) + ", cap: " + str(self.cap)
#
# class Graph:
#     def __init__(self, num):
#         self.V = num
#         self.graph = [None] * self.V
#         self.edgeTo = []
#
#     def add_edge(self, v_from, v_to, cap):
#         edge = FlowEdge(v_to, cap)
#         edge.next = self.graph[v_from]
#         self.graph[v_from] = edge
#
#     # Print the graph
#     def print_graph(self):
#         for i in range(self.V):
#             print("Vertex " + str(i) + ":", end="")
#             temp = self.graph[i]
#             while temp:
#                 print(" -> ({}, {})".format(temp.vertex, temp.cap), end="")
#                 temp = temp.next
#             print()
#
#     def has_augmenting_path(self):
#         # start with source s which is 0
#         visited, queue = set(), collections.deque([0])
#         visited.add(0)
#         self.edgeTo = [None] * self.V
#
#         while queue:
#             vertex = queue.popleft()
#             temp = self.graph[vertex]
#             while temp:
#                 if temp.vertex not in visited and temp.cap - temp.flow > 0:
#                     visited.add(temp.vertex)
#                     queue.append(temp.vertex)
#                     self.edgeTo[temp.vertex] = temp
#                 temp = temp.next
#
#         for e in self.edgeTo:
#             print(e)
#         return total_nodes - 1 in visited
#
#     def ford_fulkerson(self):
#         total_flow = 0
#         while self.has_augmenting_path():
#             bottleneck = 1000

class FlowEdge:
    def __init__(self, v, w, capacity):
        self.from_node = v
        self.to_node = w
        self.capacity = capacity
        self.flow = 0

    def other(self, vertex):
        if vertex == self.from_node:
            return self.to_node
        elif vertex == self.to_node:
            return self.from_node
        else:
            raise Exception("Error")

    def residual_capacity_to(self, vertex):
        if vertex == self.from_node:
            return self.flow
        elif vertex == self.to_node:
            return self.capacity - self.flow
        else:
            raise Exception("Error")

    def add_residual_flow_to(self, vertex, flow_to_add):
        if vertex == self.from_node:
            self.flow -= flow_to_add
        elif vertex == self.to_node:
            self.flow += flow_to_add
        else:
            raise Exception("Error")

    def __str__(self):
        return "From " + str(self.from_node) + " to " + str(self.to_node) + "; cap: " + str(self.capacity) + "; flow: " + str(self.flow)


class FlowGraph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.edgeTo = None

    def add_edge(self, e: FlowEdge):
        self.adj[e.from_node].append(e)
        self.adj[e.to_node].append(e)

    def has_augmenting_path(self):
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
                    visited.add(w)
                    queue.append(w)

        return self.V - 1 in visited

    def ford_fulkerson(self):
        while self.has_augmenting_path():  # calculates edgeTo
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

    def get_number_of_tables(self):
        tables = 0

        for i in range(1, empty_squares + 1):
            for j in range(len(self.adj[i])):
                first_edge = self.adj[i][j]
                print(first_edge)

        # for i in range(1, empty_squares + 1):
        #     for j in range(len(self.adj[i])):
        #         first_edge = self.adj[i][j]
        #         if first_edge.from_node == i:
        #             second_edge = self.adj[i][j+1]
        #             if first_edge.capacity == first_edge.flow and second_edge.capacity == second_edge.flow:
        #                 tables += 1
        #             break

        return tables


# Create graph and edges
total_nodes = empty_squares + n + m + 2
graph = FlowGraph(total_nodes)
# add edges from source to the empty squares
for i in range(1, empty_squares + 1):
    # 0 is source s
    graph.add_edge(FlowEdge(0, i, 2))

# add edges from empty squares to row and column edges
empty_squares_counter = 1
for i in range(len(trees_matrix)):
    for j in range(len(trees_matrix[0])):
        if trees_matrix[i][j] is None:
            # row
            graph.add_edge(FlowEdge(empty_squares_counter, empty_squares + i + 1, 1))
            # column
            graph.add_edge(FlowEdge(empty_squares_counter, empty_squares + n + j + 1, 1))
            empty_squares_counter += 1

# add edges from row edges to sink
for i in range(empty_squares + 1, empty_squares + 1 + n):
    # total_nodes - 1 is sink t
    graph.add_edge(FlowEdge(i, total_nodes - 1, 2))

# add edges from column edges to sink
for i in range(empty_squares + 1 + n, total_nodes - 1):
    # total_nodes - 1 is sink t
    graph.add_edge(FlowEdge(i, total_nodes - 1, 1))

graph.ford_fulkerson()

print(graph.get_number_of_tables())
