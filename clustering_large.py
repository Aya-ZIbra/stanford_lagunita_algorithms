# In this question your task is again to run the clustering algorithm from
# lecture, but on a MUCH bigger graph. So big, in fact, that the distances
# (i.e., edge costs) are only defined implicitly, rather than being provided as
# an explicit list.
#
# The data set is in clustering_big.txt.
# The format is:
# [# of nodes] [# of bits for each node's label]
# [first bit of node 1] ... [last bit of node 1]
# [first bit of node 2] ... [last bit of node 2]
# ...
#
# For example, the third line of the file
# "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1"
# denotes the 24 bits associated with node #2.
#
# The distance between two nodes u and v in this problem is defined as the
# Hamming distance--- the number of differing bits --- between the two nodes'
# labels. For example, the Hamming distance between the 24-bit label of node #2
# above and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3
# (since they differ in the 3rd, 7th, and 21st bits).
#
# The question is: what is the largest value of k such that there is a
# k-clustering with spacing at least 3? That is, how many clusters are needed
# to ensure that no pair of nodes with all but 2 bits in common get split into
# different clusters?
#
# NOTE: The graph implicitly defined by the data file is so big that you
# probably can't write it out explicitly, let alone sort the edges by cost. So
# you will have to be a little creative to complete this part of the question.
# For example, is there some way you can identify the smallest distances
# without explicitly looking at every pair of nodes?


from itertools import combinations, chain


class Node:

    def __init__(self, id, bits, parent):
        self.id = id
        self.bits = bits
        self.parent = parent


def flip_bit(bit):
    if bit == '0':
        return '1'
    elif bit == '1':
        return '0'
    else:
        raise ValueError('Bit must be either 0 or 1, not {}'.format(bit))


def generate_bits(bits, indices_to_flip):
    bits_list = list(bits)
    for i in indices_to_flip:
        bits_list[i] = flip_bit(bits_list[i])
    return ''.join(bits_list)


def nearby_nodes(nodes, node):
    # nodes that are close enough to consider for merging
    # are those that differ in 1 or 2 bits
    indices_to_flip = chain.from_iterable(
        combinations(range(0, len(node.bits)), i)
        for i in range(1, 3)
    )
    possible_bits = set([
        generate_bits(node.bits, indices)
        for indices in indices_to_flip
    ])
    actual_bits = set(nodes.keys())
    keys = actual_bits.intersection(possible_bits)
    return [nodes[key] for key in keys]


def find(nodes, node):
    # the leader node points to itself, so its bits
    # are the same as the bits of its parent
    while node.bits != node.parent:
        node = nodes[node.parent]
    return node


def union(nodes, leader_big, leader_small):
    # point the leader of the smaller connected component
    # at the leader of the larger connected component
    nodes[leader_small.bits].parent = leader_big.parent


def main():
    with open('clustering_big.txt', 'r') as f:
        num_nodes, num_bits_label = [int(n) for n in next(f).split()]
        nodes = {}
        for idx, line in enumerate(f):
            bits = ''.join(line.strip().split(' '))
            # initially, each node is its own parent
            nodes[bits] = Node(id=idx + 1,
                               bits=bits,
                               parent=bits)

        # there are duplicate lines in the file;
        # remove these to get the correct number of nodes
        num_clusters = len(nodes.keys())

        for idx, n1 in enumerate(nodes.values()):
            neighbours = nearby_nodes(nodes, n1)
            for n2 in neighbours:
                n1_leader = find(nodes, n1)
                n2_leader = find(nodes, n2)

                # 2 clusters are merged for every union
                if n1_leader != n2_leader:
                    union(nodes, n1_leader, n2_leader)
                    num_clusters -= 1

        print('There is a {}-clustering with spacing at least 3'.format(
            num_clusters,
        ))


if __name__ == '__main__':
    main()
