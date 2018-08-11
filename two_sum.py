# The goal of this problem is to implement a variant of the 2-SUM algorithm
# (covered in the Week 6 lecture on hash table applications).

# The file algo1-programming_prob-2sum.txt contains 1 million integers, both
# positive and negative (there might be some repetitions!). This is your array
# of integers, with the ith row of the file specifying the ith entry of the
# array.

# Your task is to compute the number of target values t in the interval
# [-10000,10000] (inclusive) such that there are distinct numbers x, y in the
# input file that satisfy x + y = t. (NOTE: ensuring distinctness requires a
# one-line addition to the algorithm from lecture.)

# Write your numeric answer (an integer between 0 and 20001) in the space
# provided.

# OPTIONAL CHALLENGE: If this problem is too easy for you, try implementing
#  your own hash table for it. For example, you could compare performance under
# the chaining and open addressing approaches to resolving collisions.


from bisect import bisect_left, bisect_right


def merge_sort(integers):
    # base case, no sorting needed
    if len(integers) == 1:
        return integers

    mid = len(integers) // 2
    left_half = integers[:mid]
    right_half = integers[mid:]
    # 2 recursive calls
    left_half = merge_sort(integers)
    right_half = merge_sort(integers)

    sorted_ints = []

    while len(left_half) + len(right_half) > 0:
        # if one of the arrays is empty, extend the sorted array
        # with all the elements that are left in the other array
        if len(left_half) == 0 or len(right_half) == 0:
            sorted_ints.extend(left_half)
            sorted_ints.extend(right_half)
            left_half = []
            right_half = []
        # pop off the first element of the 2 arrays that is smaller
        # and append it to the list of sorted integers
        elif left_half[0] <= right_half[0]:
            sorted_ints.append(left_half.pop(0))
        else:
            sorted_ints.append(right_half.pop(0))

    return sorted_ints


def binary_search(integers, n):
    mid = len(integers) // 2

    # base case 1
    if n == integers[mid]:
        return True
    # base case 2
    if len(integers) == 1:
        return True if integers[0] == n else False

    left_half = integers[:mid]
    right_half = integers[mid:]

    # 1 recursive call
    if n < mid:
        return binary_search(left_half, n)
    else:
        return binary_search(right_half, n)


def main():
    with open('algo1-programming_prob-2sum.txt', 'r') as f:
        integers = [int(line) for line in f]
        # Not using the merge sort algorithm implemented above
        # because of stack overflow and speed issues. Also,
        # the algorithm used to count inversions in assignment 1
        # piggybacks on merge sort. See count_inversions.py
        integers = sorted(integers)
        sets = set()

        for x in integers:
            # Not using the binary search algorithm implemented above
            # because of stack overflow and speed issues.
            left = bisect_left(integers, -10000 - x)
            right = bisect_right(integers, 10000 - x)
            integers_to_search = integers[left:right]
            sets.update(set([x + y for y in integers_to_search]))

        print('There are {} t for which distinct x + y = t.'.format(
            len(sets))
        )


if __name__ == '__main__':
    main()
