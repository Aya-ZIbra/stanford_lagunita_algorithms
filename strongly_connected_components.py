# The file SCC.txt contains the edges of a directed graph. Vertices are labeled
# as positive integers from 1 to 875714. Every row indicates an edge, the
# vertex label in first column is the tail and the vertex label in second
# column is the head (recall the graph is directed, and the edges are directed
# from the first column vertex to the second column vertex). So for example,
# the  row looks like : "2 47646". This just means that the vertex with label 2
# has an outgoing edge to the vertex with label 47646

# Your task is to code up the algorithm from the video lectures for computing
# strongly connected components (SCCs), and to run this algorithm on the given
# graph.

# Enter the sizes of the 5 largest SCCs in the given graph using the fields
# below, in decreasing order of sizes. So if your algorithm computes the sizes
# of the five largest SCCs to be 500, 400, 300, 200 and 100, enter 500 in the
# first field, 400 in the second, 300 in the third, and so on. If your
# algorithm finds less than 5 SCCs, then enter 0 for the remaining fields.
# Thus, if your algorithm computes only 3 SCCs whose sizes are 400, 300, and
# 100, then you enter 400, 300, and 100 in the first, second, and third fields,
# respectively, and 0 in the remaining 2 fields.

# WARNING: This is the most challenging programming assignment of the course.
# Because of the size of the graph you may have to manage memory carefully.#
# The best way to do this depends on your programming language and environment,
# and we strongly suggest that you exchange tips for doing this on the
# discussion forums.


from collections import defaultdict, OrderedDict


NUM_VERTICES = 875714


def depth_first_search(graph, start, explored=None, finish_order=None):
    # can't use recursive depth-first search due to stack overflow
    explored = set() if explored is None else explored
    # make use of the fact that an OrderedDict's keys are an ordered set
    # to enable element lookup in O(1) time, to prevent duplicates
    finish_order = OrderedDict() if finish_order is None else finish_order
    # keep track of the vertices that were newly visited in this iteration
    visited = set()
    stack = [start]
    while len(stack) > 0:
        vertex = stack.pop()
        if vertex not in explored:
            # if this is the first time we are seeing this vertex,
            # add it to the stack before adding its neighbours
            # so we get back to it when we've finished exploring all
            # of its neighbours
            stack.append(vertex)
            explored.add(vertex)
            to_visit = graph[vertex] - explored
            stack.extend(list(to_visit))
            visited.update(to_visit)
        elif not finish_order.get(vertex):
            # if this is the second time we are seeing this vertex,
            # we have backtracked to this vertex after exploring all
            # of its neighbours, so this vertex has FINISHED.
            finish_order[vertex] = True
    return explored, finish_order, visited


def main():
    with open('SCC.txt', 'r') as f:
        # represent the graph as a dictionary,
        # with the vertex as the key and its neighbors
        # as the list of values for that key
        graph = defaultdict(set)
        graph_reversed = defaultdict(set)
        for line in f:
            tail, head = [int(el) for el in line.strip().split()]
            # ignore self-loops
            if tail == head:
                continue
            graph[tail].add(head)
            graph_reversed[head].add(tail)

        print('Constructed graphs')

        seen = set()
        order = OrderedDict()
        # iterate through all the vertices
        # to ensure that all the vertices are explored
        for vertex in range(1, NUM_VERTICES + 1):
            if vertex not in seen:
                (
                    seen,
                    order,
                    visited,
                ) = depth_first_search(graph_reversed, vertex, seen, order)

        print('Finished 1st pass')

        explored = set()
        components = defaultdict(set)
        # iterate through the vertices in the reverse order in which
        # they finished during the first pass
        for vertex in reversed(order):
            # if we haven't explored this vertex yet, it is the leader
            # of one of the connected components in this graph
            if vertex not in explored:
                # the set of vertices visitable from the leader
                # is a strongly connected component
                (
                    explored,
                    order,
                    visited,
                ) = depth_first_search(graph, vertex, explored)
                components[vertex].add(vertex)
                components[vertex].update(visited)

        print('Finished 2nd pass')

        component_sizes = sorted([
            (key, len(values))
            for key, values in components.items()
        ], key=lambda c: c[1], reverse=True)

        print('The sizes of the top 5 SCCs are {}.'.format([
            num_components
            for leader, num_components in component_sizes[:5]]
        ))


if __name__ == '__main__':
    main()
