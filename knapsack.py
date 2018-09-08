# In this programming problem and the next you'll code up the knapsack
# algorithm from lecture.

# Let's start with a warm-up. The file knapsack1.txt describes a knapsack
# instance, and it has the following format:
# [knapsack_size][number_of_items]
# [value_1] [weight_1]
# [value_2] [weight_2]
# ...

# For example, the third line of the file is "50074 659", indicating that the
# second item has value 50074 and size 659, respectively.

# You can assume that all numbers are positive. You should assume that item
# weights and the knapsack capacity are integers.

# ADVICE: If you're not getting the correct answer, try debugging your
# algorithm using some small test cases. And then post them to the discussion
# forum!


class Item:

    def __init__(self, value=0, weight=0):
        self.value = value
        self.weight = weight


def knapsack(items, capacity):
    # 2D array that stores the optimal solutions to subproblems
    # rows: index for each item (0 means no item)
    # columms: usable capacity of the knapsack
    memo = [
        [None for i in range(len(items) + 1)]
        for c in range(capacity + 1)
    ]

    # if there is no item, the optimal solution is 0
    for c in range(capacity + 1):
        memo[c][0] = 0

    for i, item in enumerate(items):
        for c in range(capacity + 1):
            # 1st possibility: last item is not in the optimal solution
            # 2nd possibility: last item is in the optimal solution
            p1 = memo[c][i]
            p2 = item.value + memo[c - item.weight][i]
            # if the item's weight exceeds the usable capacity,
            # we're forced to exclude it
            if item.weight > c:
                memo[c][i+1] = memo[c][i]
            # otherwise, choose the better of the 2 possibilities
            else:
                memo[c][i+1] = max(p1, p2)

    # the optimal solution is the value in the last row and column
    return memo[capacity][len(items)]


def main():
    with open('knapsack1.txt', 'r') as f:
        capacity, num_items = [int(n) for n in next(f).split()]
        items = []
        for line in f:
            value, weight = line.split()
            items.append(Item(value=int(value),
                              weight=int(weight)))
        max_value = knapsack(items, capacity)
        print('The value of the optimal solution is {}'.format(max_value))


if __name__ == '__main__':
    main()
