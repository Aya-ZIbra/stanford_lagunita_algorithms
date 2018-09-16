# The file dijkstraData.txt contains an adjacency list representation of an
# undirected weighted graph with 200 vertices labeled 1 to 200. Each row
# consists of the node tuples that are adjacent to that particular vertex along
# with the length of that edge. For example, the 6th row has 6 as the first
# entry indicating that this row corresponds to the vertex labeled 6. The next
# entry of this row "141,8200" indicates that there is an edge between vertex 6
# and vertex 141 that has length 8200. The rest of the pairs of this row
# indicate the other vertices adjacent to vertex 6 and the lengths of the
# corresponding edges.

# Your task is to run Dijkstra's shortest-path algorithm on this graph, using 1
# (the first vertex) as the source vertex, and to compute the shortest-path
# distances between 1 and every other vertex of the graph. If there is no path
# between a vertex and vertex 1, we'll define the shortest-path distance
# between 1 and v to be 1000000.

# You should report the shortest-path distances to the following ten vertices,
# in order: 7,37,59,82,99,115,133,165,188,197. Enter the shortest-path
# distances using the fields below for each of the vertices.

# IMPLEMENTATION NOTES: This graph is small enough that the straightforward
# O(mn) time implementation of Dijkstra's algorithm should work fine.

# OPTIONAL: For those of you seeking an additional challenge, try implementing
# the heap-based version. Note this requires a heap that supports deletions,
# and you'll probably need to maintain some kind of mapping between vertices
# and their positions in the heap.


import math
from collections import defaultdict


NUM_VERTICES = 200
VERTICES_TO_CHECK = [7, 37, 59, 82,  99, 115, 133, 165, 188, 197]


class Node:
    """Implementation of a node.
       The node keeps track of its own label and key (weight)."""
    def __init__(self, label, key):
        self.label = label
        self.key = key

    def __repr__(self):
        return 'Node(label={}, key={})'.format(self.label, self.key)


class Heap:
    """Implmentation of a heap.
       Every node must have a key that is <= the keys of its children.
    """
    def __init__(self):
        self.nodes = []

    def is_empty(self):
        return True if len(self.nodes) == 0 else False

    def get_node(self, label):
        # only works if all the labels are unique
        for idx, node in enumerate(self.nodes):
            if node.label == label:
                return node, idx
        return None, None

    def parent(self, node, idx):
        # this is the root, it has no parent
        if idx == 0:
            return None, None
        elif idx % 2 == 0:
            idx = idx - 1
        parent_idx = int(math.floor(idx / 2))
        parent = self.nodes[parent_idx]
        return parent, parent_idx

    def children(self, node, idx):
        left_idx = 2 * idx + 1
        right_idx = 2 * idx + 2
        max_idx = len(self.nodes) - 1
        left_child = self.nodes[left_idx] if left_idx <= max_idx else None
        right_child = self.nodes[right_idx] if right_idx <= max_idx else None
        return (left_child, left_idx), (right_child, right_idx)

    def insert(self, node):
        # insert the node at the end and
        # recursively bubble upwards
        self.nodes.append(node)
        idx = len(self.nodes) - 1
        self.bubble_up(node, idx)

    def delete(self, label):
        # if the node is in the heap, replace it with
        # the last node, then recursively bubble up or down
        node, idx = self.get_node(label)
        if node is not None:
            last_node = self.nodes[-1]
            self.nodes[idx] = last_node
            self.nodes.pop()
            parent, parent_idx = self.parent(last_node, idx)
            # bubble up if the parent key is greater than the node key
            if parent and parent.key > last_node.key:
                self.bubble_up(last_node, idx)
            # bubble down if the parent is the root node
            # or the parent key is less than the node key
            else:
                self.bubble_down(last_node, idx)

    def extract_min(self):
        min_node = self.nodes[0]
        self.delete(min_node.label)
        return min_node

    def bubble_up(self, node, idx):
        parent, parent_idx = self.parent(node, idx)
        if parent and parent.key > node.key:
            # swap recursively until the node has
            # a parent that is smaller than itself
            self.nodes[idx] = parent
            self.nodes[parent_idx] = node
            self.bubble_up(node, parent_idx)

    def bubble_down(self, node, idx):
        (
            (left_child, left_idx),
            (right_child, right_idx)
        ) = self.children(node, idx)

        # swap with the smallest child recursively until
        # the node is smaller than both of its children
        if (
            left_child and node.key > left_child.key or
            right_child and node.key > right_child.key
        ):
            if not right_child or left_child.key < right_child.key:
                self.nodes[left_idx] = node
                self.nodes[idx] = left_child
                self.bubble_down(node, left_idx)
            elif not left_child or right_child.key < left_child.key:
                self.nodes[right_idx] = node
                self.nodes[idx] = right_child
                self.bubble_down(node, right_idx)


def dijkstra(edges, num_vertices, source):
    heap = Heap()
    processed = [source]
    shortest_dists = defaultdict(lambda: float('inf'))
    shortest_dists[source] = 0

    # to start, populate the heap with all the nodes
    # that the source vertex is connected to
    for v, w in edges[source].items():
        heap.insert(Node(label=v, key=w))
    # the nodes which the source vertex aren't connected to
    # each have the maximum possible weight (infinity)
    for n in range(2, num_vertices + 1):
        if n not in edges[source].keys():
            heap.insert(Node(label=n, key=float('inf')))

    while not heap.is_empty():
        closest_node = heap.extract_min()
        processed.append(closest_node.label)
        shortest_dists[closest_node.label] = closest_node.key
        # for each node connected to the node that was just extracted,
        # delete it from the heap, re-compute its weight / key value,
        # then insert the new node into the heap
        for v, w in edges[closest_node.label].items():
            if v not in processed:
                v_node, v_idx = heap.get_node(label=v)
                heap.delete(v)
                # the new weight is the smaller of the current weight and the
                # current shortest distance plus this edge's weight
                new_w = min(v_node.key, shortest_dists[closest_node.label] + w)
                heap.insert(Node(label=v, key=new_w))

    return shortest_dists


def main():
    with open('dijkstraData.txt', 'r') as f:
        # store the graph as a dictionary of edges, where
        # the keys are the vertices and for each vertex,
        # the value is a nested dictionary of key-value pairs,
        # with the key being the vertex on the other side of
        # the edge and the value being the weight of that edge
        edges = defaultdict(dict)
        source = 1

        for line in f:
            line = line.split()
            v1, rest = int(line[0]), line[1:]
            for edge in rest:
                v2, weight = [int(n) for n in edge.split(',')]
                edges[v1][v2] = weight

        shortest_distances = dijkstra(edges, NUM_VERTICES, source)
        for vertex in VERTICES_TO_CHECK:
            print('Shortest distance between vertices {} and {}: {}'.format(
                source,
                vertex,
                shortest_distances[vertex],
            ))


if __name__ == '__main__':
    main()
