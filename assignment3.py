# The file kargerMinCut.txt contains the adjacency list representation of a
# simple undirected graph. There are 200 vertices labeled 1 to 200. The first
# column in the file represents the vertex label, and the particular row
# (other entries except the first column) tells all the vertices that the
# vertex is adjacent to. So for example, the 6th row looks like:
# "6 155 56 52 120 ......". This just means that the vertex with label 6 is
# adjacent to (i.e., shares an edge with) the vertices with labels
# 155,56,52,120,......,etc

# Your task is to code up and run the randomized contraction algorithm for the
# min cut problem and use it on the above graph to compute the min cut.
# (HINT: Note that you'll have to figure out an implementation of edge
# contractions. Initially, you might want to do this naively, creating a new
# graph from the old every time there's an edge contraction. But you should
# also think about more efficient implementations.)

# (WARNING: As per the video lectures, please make sure to run the algorithm
# many times with different random seeds, and remember the smallest cut that
# you ever find.)


import random


def get_edges(graph):
    edges = []
    for vertex in graph.keys():
        edges.extend([
            (vertex, adjacent_vertex)
            for adjacent_vertex in graph[vertex]
        ])
    return edges


def merge_vertices(graph, v1, v2):
    # remove the edge connecting v1 and v2
    graph[v1].remove(v2)
    graph[v2].remove(v1)
    # the new vertex is the new largest number
    current_max = max(graph.keys())
    new_vertex = current_max + 1
    # the new vertex can have >1 edge with another vertex
    # but cannot have self-loops
    graph[new_vertex] = graph[v1] + graph[v2]
    # update the new vertex everywhere in the graph
    for vertex in graph.keys():
        for v in [v1, v2]:
            if v in graph[vertex]:
                graph[vertex] = [
                    vert if vert != v else new_vertex
                    for vert in graph[vertex]
                ]
    # remove self-loops
    graph[new_vertex] = [
        vert for vert in graph[new_vertex]
        if vert != new_vertex
    ]
    # delete the old vertices
    del graph[v1]
    del graph[v2]
    return graph


def compute_min_cut(graph):
    num_vertices = len(graph.keys())
    edges = get_edges(graph)
    # merge 2 vertices until there are only 2 vertices left
    while num_vertices > 2:
        # select the edge to remove
        chosen_edge = random.choice(edges)
        # merge the vertices that this edge comprises
        graph = merge_vertices(graph, *chosen_edge)
        edges = get_edges(graph)
        num_vertices = len(graph.keys())
    # each edge is represented twice, so divide by 2
    # to get the number of edges remaining in the graph
    return len(edges) / 2


def main():
    with open('kargerMinCut.txt', 'r') as f:
        # represent the graph with a dict, where the key is the vertex
        # and the value is a list of all of the vertices it shares edges with
        graph = dict()
        for line in f:
            vertices = [int(v) for v in line.split()]
            vertex, adjacents = vertices[0], vertices[1:]
            graph[vertex] = adjacents
        # to maximize the probability of getting the minimum cut,
        # run the algorithm to compute the min cut n^2 times
        # where n is the number of vertices in the graph
        num_vertices = len(graph.keys())
        smallest = None
        for i in range(0, num_vertices**2):
            min_cut = compute_min_cut(graph)
            if smallest is None or min_cut < smallest:
                smallest = min_cut
        print('The min cut is {}.'.format(smallest))


if __name__ == '__main__':
    main()
