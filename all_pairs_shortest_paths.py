# In this assignment you will implement one or more algorithms for the
# all-pairs shortest-path problem. Here are data files describing three graphs:
# g1.txt, g2.txt, g3.txt

# The first line indicates the number of vertices and edges, respectively. Each
# subsequent line describes an edge (the first two numbers are its tail and
# head, respectively) and its length (the third number).

# NOTE: some of the edge lengths are negative.
# NOTE: These graphs may or may not have negative-cost cycles.

# Your task is to compute the shortest shortest path. Precisely, you must first
# identify which, if any, of the three graphs have no negative cycles. For each
# such graph, you should compute all-pairs shortest paths and remember the
# smallest one (i.e., compute min(u,v) d(u,v) where d(u,v) denotes the
# shortest-path distance from u to v).

# If each of the three graphs has a negative-cost cycle, then enter "NULL" in
# the box below. If exactly one graph has no negative-cost cycles, then enter
# the length of its shortest shortest path in the box below. If two or more of
# the graphs have no negative-cost cycles, then enter the smallest of the
# lengths of their shortest shortest paths in the box below.

# OPTIONAL: You can use whatever algorithm you like to solve this question. If
# you have extra time, try comparing the performance of different all-pairs
# shortest-path algorithms!

# OPTIONAL: Here is a bigger data set to play with: large.txt. For fun, try
# computing the shortest shortest path of the graph in the file above.


from collections import defaultdict
from dijkstra import dijkstra


def bellman_ford(graph, num_vertices, source):
    # prev_dist: shortest path distance with at most i-1 hops
    # curr_dist: shortest path distance with at most i hops
    # predecessor: second-to-last vertex on the shortest path
    prev_distances = [float('inf')]
    curr_distances = [float('inf')]
    predecessors = [None]

    # at the beginning, all vertices have a distance of infinity
    # and no predecessor
    for v in range(num_vertices):
        prev_distances.append(float('inf'))
        curr_distances.append(float('inf'))
        predecessors.append(None)

    # the distance of the source to itself is 0
    prev_distances[source] = 0
    curr_distances[source] = 0

    # perform an extra iteration in order to detect negative cost cycles
    for i in range(1, num_vertices + 1):
        # the distance with at most i hops is the minimum of
        # the distance with at most i-1 hops to the vertex and
        # the distances with at most i-1 hops to a neighbouring vertex
        # plus the weight of edge connecting the neighbour to the vertex
        curr_distances[i] = prev_distances[i]
        predecessors[i] = predecessors[i]
        for tail in graph[i]:
            weight = graph[i][tail]
            if prev_distances[tail] + weight < curr_distances[i]:
                curr_distances[i] = prev_distances[tail] + weight
                predecessors[i] = tail
        # cache the results of the current iteration for the next iteration
        prev_distances = curr_distances

    # if the shortest path distance for any vertex has changed after the
    # nth iteration, the graph contains a negative cost cycle, so bail out
    if prev_distances != curr_distances:
        raise AssertionError('The graph contains a negative cost cycle!')
    # otherwise, return the shortest path distances and predecessors
    return curr_distances, predecessors


def johnson(graph, num_vertices):
    shortest_distances = {}
    # add a new vertex 0 to the graph that is
    # connected to all of the other vertices with weight 0
    for i in range(1, num_vertices):
        graph[i][0] = 0

    # run the Bellman-Ford algorithm on the graph with vertex 0 as the source
    # to find the shortest path distances from the source vertex to each of the
    # other vertices. If a negative cycle is detected, terminate the algorithm
    try:
        distances, predecessors = bellman_ford(graph, num_vertices, 0)
        # remove the vertex 0 from the graph
        for i in range(1, num_vertices):
            del graph[i][0]
        reversed_graph = reverse_graph(graph)
        for i in range(1, num_vertices):
            # re-weight the edges of the original graph using the values
            # computed by the Bellman-Ford algorithm, to w(u, v) + h(u) - h(v)
            for tail in graph[i]:
                graph[i][tail] += distances[tail] - distances[i]
            # run Dijkstra's algorithm n times to find the shortest path
            # distances from each vertex to every other vertex
            shortest_distances[i] = dijkstra(reversed_graph, num_vertices, i)
        return shortest_distances
    except AssertionError as err:
        print(str(err))


def make_graph(filename):
    # represent the graph as a nested dictionary
    # the keys are the head vertices and the values are
    # another dictionary in which the keys are
    # the tail vertices which lead to the head vertices and
    # the values are the weights of the edges
    graph = defaultdict(dict)
    with open(filename, 'r') as f:
        num_vertices, num_edges = [int(n) for n in next(f).split()]
        for line in f:
            tail, head, weight = [int(n) for n in line.split()]
            graph[head][tail] = weight
    return graph, num_vertices


def reverse_graph(graph):
    reversed_graph = defaultdict(dict)
    for head in graph.keys():
        for tail in graph[head]:
            reversed_graph[tail][head] = graph[head][tail]
    return reversed_graph


def main():
    # filenames = ['g1.txt', 'g2.txt', 'g3.txt']
    # for filename in filenames:
    #     graph, num_vertices = make_graph(filename)
    #     print(johnson(graph, num_vertices))
    graph = {
        1: {},
        2: {
            1: 2,  # s -> v: 2
        },
        3: {
            1: 4,  # s -> x: 4
            2: 1,  # v -> x: 1
        },
        4: {
            2: 2,  # v -> w: 2
        },
        5: {
            3: 4,  # x -> t: 4
            4: 2,  # w -> t: 2
        },
    }
    print(johnson(graph, 5))


if __name__ == '__main__':
    main()
