# The file edges.txt describes an undirected graph with integer edge costs.
# It has the format
#
# [number_of_nodes] [number_of_edges]
# [one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]
# [one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]
# ...
#
# For example, the third line of the file is "2 3 -8874", indicating that there
# is an edge connecting vertex #2 and vertex #3 that has cost -8874.
#
# You should NOT assume that edge costs are positive, nor should you assume
# that they are distinct.
#
# Your task is to run Prim's minimum spanning tree algorithm on this graph.
#
# You should report the overall cost of a minimum spanning tree --- an integer,
# which may or may not be negative --- in the box below.
#
# IMPLEMENTATION NOTES: This graph is small enough that the straightforward
# O(mn) time implementation of Prim's algorithm should work fine.
#
# OPTIONAL: For those of you seeking an additional challenge, try implementing
# a heap-based version. The simpler approach, which should already give you a
# healthy speed-up, is to maintain relevant edges in a heap (with keys = edge
# costs). The superior approach stores the unprocessed vertices in the heap, as
# described in lecture. Note this requires a heap that supports deletions, and
# you'll probably need to maintain some kind of mapping between vertices and
# their positions in the heap.


from collections import defaultdict
from dijkstra import Heap, Node


def prim(edges, num_nodes):
    # choose a vertex to start with
    source = 1
    processed = set([source])
    total_cost = 0

    heap = Heap()
    # to start, populate the heap with all the nodes
    # that the source vertex is connected to
    for v, c in edges[source].items():
        heap.insert(Node(label=v, key=c))
    # the nodes which the source vertex aren't connected to
    # each have the maximum possible weight (infinity)
    for n in range(2, num_nodes + 1):
        if n not in edges[source].keys():
            heap.insert(Node(label=n, key=float('inf')))

    while not heap.is_empty():
        node = heap.extract_min()
        processed.add(node.label)
        total_cost += node.key
        # every edge with the current vertex at one end
        # and the other vertex still in the heap (not yet processed)
        # is an edge crossing the new cut
        for v, c in edges[node.label].items():
            if v not in processed:
                # recompute the cheapest cost for each vertex
                # in the cut and on the other end of a processed vertex
                v_node, v_idx = heap.get_node(label=v)
                heap.delete(v)
                new_c = min(v_node.key, c)
                heap.insert(Node(label=v, key=new_c))

    return total_cost


def main():
    with open('edges.txt', 'r') as f:
        # store the graph as a dictionary of edges, where
        # the keys are the vertices and for each vertex,
        # the value is a nested dictionary of key-value pairs,
        # with the key being the vertex on the other side of
        # the edge and the value being the cost of that edge
        edges = defaultdict(dict)

        num_nodes, num_edges = [int(n) for n in next(f).split()]

        for line in f:
            v1, v2, cost = [int(n) for n in line.split()]
            edges[v1][v2] = cost
            edges[v2][v1] = cost

        print('The overall cost of the minimum spanning tree is {}'.format(
            prim(edges, num_nodes)
        ))


if __name__ == '__main__':
    main()
