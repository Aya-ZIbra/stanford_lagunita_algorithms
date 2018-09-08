# This problem also asks you to solve a knapsack instance, but a much bigger
# one.

# The file knapsack_big.txt describes a knapsack instance,
# and it has the following format:
# [knapsack_size][number_of_items]
# [value_1] [weight_1]
# [value_2] [weight_2]
# ...

# For example, the third line of the file is "50074 834558", indicating that
# the second item has value 50074 and size 834558, respectively. As before, you
# should assume that item weights and the knapsack capacity are integers.

# This instance is so big that the straightforward iterative implemetation uses
# an infeasible amount of time and space. So you will have to be creative to
# compute an optimal solution. One idea is to go back to a recursive
# implementation, solving subproblems --- and, of course, caching the results
# to avoid redundant work --- only on an "as needed" basis. Also, be sure to
# think about appropriate data structures for storing and looking up solutions
# to subproblems.

# ADVICE: If you're not getting the correct answer, try debugging your
# algorithm using some small test cases. And then post them to the discussion
# forum!


import sys
sys.setrecursionlimit(20000)


MEMO = {}


class Item:

    def __init__(self, value=0, weight=0):
        self.value = value
        self.weight = weight


def knapsack(items, idx, capacity):
    # cache only the item idx and capacity for space efficiency
    if (idx, capacity) not in MEMO:
        # base case: if there are no items, the max value is 0
        if idx == 0:
            MEMO[(idx, capacity)] = 0
        else:
            item = items[idx]
            # if the item's weight exceeds the usable capacity,
            # we're forced to exclude it
            if item.weight > capacity:
                MEMO[(idx, capacity)] = knapsack(items, idx - 1, capacity)
            # otherwise, we may be able to select the item;
            # choose the better of the 2 possibilities
            else:
                MEMO[(idx, capacity)] = max(
                    knapsack(items, idx - 1, capacity),
                    knapsack(items, idx - 1, capacity - item.weight) + item.value,
                )
    return MEMO[(idx, capacity)]


def main():
    with open('knapsack_big.txt', 'r') as f:
        capacity, num_items = [int(n) for n in next(f).split()]
        items = [Item(value=0, weight=0)]
        for line in f:
            value, weight = line.split()
            items.append(Item(value=int(value),
                              weight=int(weight)))
        max_value = knapsack(items, num_items, capacity)
        print('The value of the optimal solution is {}'.format(max_value))


if __name__ == '__main__':
    main()
