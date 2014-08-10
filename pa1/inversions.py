#!/usr/bin/env python3

"""
Implementation of the Merge Sort algorithm in order to
count the number of inversions in a list of integers.
"""

import argparse

def read_file(filename):
    with open(filename) as f:
        return [int(line) for line in f]

def _merge_sort(A, B, begin, end):
    if end - begin < 2:
        return
    middle = begin + (end - begin)//2
    _merge_sort(A, B, begin, middle)
    _merge_sort(A, B, middle, end)
    merge(A, B, begin, middle, end)
    A[begin:end] = B[begin:end]

def merge(A, B, begin, middle, end):
    global inversions
    i, j = begin, middle
    for k in range(begin, end):
        if i < middle and (j >= end or A[i] <= A[j]):
            B[k] = A[i]
            i += 1
        else:
            inversions += middle - i
            B[k] = A[j]
            j += 1

def merge_sort(A):
    _merge_sort(A, A[:], 0, len(A))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute number of inversions.")
    parser.add_argument('filename',
                        type=str,
                        help="file containing list of integers")

    args = parser.parse_args()

    integer_list = read_file(args.filename)
    inversions = 0
    merge_sort(integer_list)
    print(inversions)
