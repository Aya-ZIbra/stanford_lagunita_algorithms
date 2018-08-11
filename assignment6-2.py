# The goal of this problem is to implement the "Median Maintenance" algorithm
# (covered in the Week 5 lecture on heap applications). The text file contains
# a list of the integers from 1 to 10000 in unsorted order; you should treat
# this as a stream of numbers, arriving one by one.

# Letting xi denote the ith number of the file, the th median mk is defined as
# the median of the numbers x1 ... xk. (So, if k is odd, then k is the
# ((k+1)/2)th smallest number among x1 ... xk; if k is even, then mk is the
# (k/2)th smallest number among x1 ... xk.)

# In the box below you should type the sum of these 10000 medians, modulo 10000
# (i.e., only the last 4 digits). That is, you should compute
# (m1 + m2 + m3 + ... + m10000) mod 10000.

# OPTIONAL EXERCISE: Compare the performance achieved by heap-based and
# search-tree-based implementations of the algorithm.


import math


class Heap:
    """Implmentation of a min heap.
       Every node must have a key that is <= the keys of its children.
    """
    def __init__(self):
        self.nodes = []

    def size(self):
        return len(self.nodes)

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

    def root(self):
        if self.size() > 0:
            return self.nodes[0]

    def insert(self, node):
        # insert the node at the end and
        # recursively bubble upwards
        self.nodes.append(node)
        idx = self.size() - 1
        self.bubble_up(node, idx)

    def extract_root(self):
        root_node = self.nodes[0]
        last_node = self.nodes[-1]
        self.nodes[0] = last_node
        self.nodes.pop()
        self.bubble_down(last_node, 0)
        return root_node

    def bubble_up(self, node, idx):
        parent, parent_idx = self.parent(node, idx)
        if parent and parent > node:
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
            left_child and node > left_child or
            right_child and node > right_child
        ):
            if not right_child or left_child < right_child:
                self.nodes[left_idx] = node
                self.nodes[idx] = left_child
                self.bubble_down(node, left_idx)
            elif not left_child or right_child < left_child:
                self.nodes[right_idx] = node
                self.nodes[idx] = right_child
                self.bubble_down(node, right_idx)


def main():
    with open('Median.txt', 'r') as f:
        # contains the largest numbers
        high_heap = Heap()
        # contains the smallest numbers
        low_heap = Heap()
        median_sum = 0
        medians = []

        for idx, line in enumerate(f):
            integer = int(line)
            # the smallest element of the largest numbers
            high_root = high_heap.root()

            if high_root is None:
                high_heap.insert(integer)
            # if the integer is bigger than the high root,
            # stick it in the high heap (largest numbers)
            elif integer > high_root:
                high_heap.insert(integer)
            # otherwise stick it in the low heap (smallest numbers)
            else:
                low_heap.insert(-integer)

            # if the heaps are unbalanced, rebalance by
            # removing one node from the bigger heap and
            # inserting it into the smaller heap
            if high_heap.size() - low_heap.size() > 1:
                node = high_heap.extract_root()
                low_heap.insert(-node)
            elif low_heap.size() - high_heap.size() > 1:
                node = -low_heap.extract_root()
                high_heap.insert(node)

            # the total number of integers seen so far is even
            # this means that the 2 heaps have the same size
            if high_heap.size() + low_heap.size() % 2 == 0:
                median = low_heap.root()
            # the total number of integers seen so far is odd
            # this means that 1 heap has 1 more node than the other
            else:
                # the high heap is the heap with the extra node
                if high_heap.size() > low_heap.size():
                    median = high_heap.root()
                # the low heap is the heap with the extra node
                else:
                    median = -low_heap.root()

            medians.append(median)
            median_sum += median

        print('The sum of the medians mod 10,000 is {}.'.format(
            sum(medians) % 10000,
        ))


if __name__ == '__main__':
    main()
