# The file QuickSort.txt contains all of the integers between 1 and 10,000
# (inclusive, with no repeats) in unsorted order. The integer in the ith row of
# the file gives you the ith entry of an input array.

# Your task is to compute the total number of comparisons used to sort the
# given input file by QuickSort. As you know, the number of comparisons depends
# on which elements are chosen as pivots, so we'll ask you to explore three
# different pivoting rules.

# You should not count comparisons one-by-one. Rather, when there is a
# recursive call on a subarray of length m, you should simply add m-1 to your
# running total of comparisons. (This is because the pivot element is compared
# to each of the other m-1 elements in the subarray in this recursive call.)

# WARNING: The Partition subroutine can be implemented in several different
# ways, and different implementations can give you differing numbers of
# comparisons. For this problem, you should implement the Partition subroutine
# exactly as it is described in the video lectures (otherwise you might get the
# wrong answer).


# 1) For the first part of the programming assignment, you should always use
# the first element of the array as the pivot element.

# 2) Compute the number of comparisons (as in Problem 1), always using the
# final element of the given array as the pivot element. Again, be sure to
# implement the Partition subroutine exactly as it is described in the video
# lectures.

# Recall from the lectures that, just before the main Partition subroutine,
# you should exchange the pivot element (i.e., the last element) with the first
# element.

# 3) Compute the number of comparisons (as in Problem 1), using the
# "median-of-three" pivot rule. [The primary motivation behind this rule is to
# do a little bit of extra work to get much better performance on input arrays
# that are nearly sorted or reverse sorted.] In more detail, you should choose
# the pivot as follows.

# Consider the first, middle, and final elements of the given array.
# (If the array has odd length it should be clear what the "middle" element is;
# for an array with even length 2k, use the kth element as "middle" element.
# So for the array 4 5 6 7, the "middle" element is the the second one ----
# 5 and not 6!)

# Identify which of these three elements is the median (i.e., the one whose
# value is in between the other two), and use this as your pivot. As discussed
# in the first and second parts of this programming assignment, be sure to
# implement Partition exactly as described in the video lectures (including
# exchanging the pivot element with the first element just before the main
# Partition subroutine).

# EXAMPLE: For the input array 8 2 4 5 7 1 you would consider the first (8),
# middle (4), and last (1) elements; since 4 is the median of the set {1,4,8},
# you would use 4 as your pivot element.

# SUBTLE POINT: A careful analysis would keep track of the comparisons made in
# identifying the median of the three candidate elements. You should NOT do
# this. That is, as in the previous two problems, you should simply add m-1 to
# your running total of comparisons every time you recurse on a subarray with
# length m.


PIVOT_TYPES = ['FIRST', 'LAST', 'MEDIAN']


def pick_pivot(integers, pivot_type):
    first = integers[0]
    last = integers[-1]
    # if there is an even number of integers 2k,
    # pick the kth element as the middle element
    middle = integers[(len(integers) - 1) // 2]

    # swap the selected pivot with the first element
    # so the pivot is always in the first position
    if pivot_type == 'FIRST':
        return first, integers
    elif pivot_type == 'LAST':
        integers[0], integers[-1] = integers[-1], integers[0]
        return last, integers
    elif pivot_type == 'MEDIAN':
        pivot = sorted([first, last, middle])[1]
        pivot_idx = integers.index(pivot)
        integers[0], integers[pivot_idx] = integers[pivot_idx], integers[0]
        return pivot, integers
    else:
        raise ValueError('Pivot type must be one of ', PIVOT_TYPES)


def partition(integers, pivot_type):
    # base case; need at least 2 integers for comparison
    if len(integers) <= 1:
        return 0

    pivot, integers = pick_pivot(integers, pivot_type)
    i = 1

    for j in range(i, len(integers)):
        curr = integers[j]
        # if the current element is smaller than the pivot,
        # swap the current element and the element to the immediate
        # right of the pivot so that the current element ends up
        # to the left of the pivot, then advance i by 1
        if curr < pivot:
            integers[i], integers[j] = curr, integers[i]
            i += 1
        # if the current element is bigger than the pivot
        # do nothing since it's already to the right of the pivot
        elif curr > pivot:
            continue

    # finally, swap the pivot into its rightful position
    integers[0], integers[i - 1] = integers[i - 1], integers[0]

    left_of_pivot = integers[0:i-1]
    left_comparisons = partition(left_of_pivot, pivot_type)

    right_of_pivot = integers[i:len(integers)]
    right_comparisons = partition(right_of_pivot, pivot_type)

    return sum([len(integers) - 1, left_comparisons, right_comparisons])


def main():
    for pivot_type in PIVOT_TYPES:
        with open('QuickSort.txt', 'r') as f:
            integers = [int(line) for line in f]
            num_comparisons = partition(integers, pivot_type)
            print('There are {} comparisons with the {} pivot type.'.format(
                num_comparisons,
                pivot_type,
            ))


if __name__ == '__main__':
    main()
