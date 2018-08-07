# The file IntegerArray.txt contains all of the 100,000 integers between 1 and
# 100,000 (inclusive) in some order, with no integer repeated.

# Your task is to compute the number of inversions in the file given, where the
# row of the file indicates the  entry of an array.

# Because of the large size of this array, you should implement the fast
# divide-and-conquer algorithm covered in the video lectures.


def sort_count_inversions(integers):
    # base case, no inversion if there is only 1 integer
    if len(integers) == 1:
        return integers, 0

    mid = len(integers) // 2
    left = integers[:mid]
    right = integers[mid:]
    # 2 recursive calls
    left, left_inversions = sort_count_inversions(left)
    right, right_inversions = sort_count_inversions(right)

    sorted_ints = []
    split_inversions = 0

    while len(left) + len(right) > 0:
        # if one of the arrays is empty, extend the sorted array
        # with all the elements that are left in the other array
        if len(left) == 0 or len(right) == 0:
            sorted_ints.extend(left)
            sorted_ints.extend(right)
            left = []
            right = []
        # if the first element of the left array is smaller,
        # there is no inversion
        elif left[0] <= right[0]:
            sorted_ints.append(left.pop(0))
        # if the first element of the right array is smaller,
        # there is at least one inversion!
        # (specifically, all the remaining elements in the left array)
        else:
            sorted_ints.append(right.pop(0))
            split_inversions += len(left)

    assert len(sorted_ints) == len(integers)
    return sorted_ints, sum([left_inversions, right_inversions, split_inversions])


def main():
    with open('IntegerArray.txt', 'r') as f:
        integers = [int(line) for line in f]
        sorted_ints, num_inversions = sort_count_inversions(integers)
        print('There are {} inversions.'.format(num_inversions))


if __name__ == '__main__':
    main()
