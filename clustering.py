# In this programming problem and the next you'll code up the clustering
# algorithm from lecture for computing a max-spacing k-clustering.
#
# The file clustering1.txt describes a distance function
# (equivalently, a complete graph with edge costs).
# It has the following format:
#
# [number_of_nodes]
# [edge 1 node 1] [edge 1 node 2] [edge 1 cost]
# [edge 2 node 1] [edge 2 node 2] [edge 2 cost]
# ...
#
# There is one edge (i, j) for each choice of 1 <= i < j <= n,
# where n is the number of nodes.
#
# For example, the third line of the file is "1 3 5250", indicating that the
# distance between nodes 1 and 3 (equivalently, the cost of the edge (1,3)) is
# 5250. You can assume that distances are positive, but you should NOT assume
# that they are distinct.
#
# Your task in this problem is to run the clustering algorithm from lecture on
# this data set, where the target number k of clusters is set to 4.
# What is the maximum spacing of a 4-clustering?


from collections import Counter

DESIRED_NUM_CLUSTERS = 4


def find(forest, node):
    # the leader node points to itself, so its value
    # is the same number as its position in the forest
    while node != forest[node]:
        node = forest[node]
    return node


def union(forest, leader_big, leader_small):
    # point the leader of the smaller connected component
    # at the leader of the larger connected component
    forest[leader_small] = leader_big


def main():
    with open('clustering1.txt', 'r') as f:
        num_nodes = int(next(f))
        nodes = range(1, num_nodes + 1)
        # sort edges by cost, in ascending order
        edges = sorted([
            [int(n) for n in line.split()]
            for line in f
        ], key=lambda e: e[2])

        # forests are represented compactly in memory as arrays
        # in which leaders are indicated by the array index
        # initially, each node is its own parent / leader
        # make the first element 0 so that each node's index
        # is the node's parent
        forest = [0] + nodes
        num_clusters = num_nodes

        while num_clusters > DESIRED_NUM_CLUSTERS:
            # consider the cheapest remaining edge
            v1, v2, cost = edges.pop(0)
            v1_leader = find(forest, v1)
            v2_leader = find(forest, v2)

            # if the nodes do not have the same leader,
            # they are in different connected components,
            # so adding this edge will not create a cycle
            if v1_leader != v2_leader:
                sizes = Counter(forest[1:])
                v1_size = sizes[v1_leader]
                v2_size = sizes[v2_leader]

                # make the elements of the smaller connected component
                # point to the leader of the larger connected component
                if v1_size >= v2_size:
                    union(forest, v1_leader, v2_leader)
                else:
                    union(forest, v2_leader, v1_leader)

                # 2 clusters are merged every time an edge is added
                num_clusters -= 1

        # remove more internal edges
        done = False
        while not done:
            n1, n2, dist = edges.pop(0)
            n1_leader = find(forest, n1)
            n2_leader = find(forest, n2)
            # the distance of the first external edge is the max spacing
            if n1_leader != n2_leader:
                done = True

        print('The maximum spacing of the 4-clustering is {}'.format(dist))


if __name__ == '__main__':
    main()
