#!/usr/bin/env python3

"""
Implementation of Quicksort in order to compute the total number of comparisons
used to sort a given list of integers using different pivot-choosing rules.
"""

import argparse

def swap(A, i, j):
    A[i], A[j] = A[j], A[i]

def choose_first(A, left, right):
    return left

def choose_last(A, left, right):
    return right

def choose_median(A, left, right):
    middle = (left + right)//2
    value_to_position = {A[left]: left, A[middle]: middle, A[right]: right}
    return value_to_position[sorted(value_to_position)[1]]

def partition(A, left, right, pivot_index):
    pivot = A[pivot_index]
    i = left + 1
    swap(A, left, pivot_index)
    for j in range(left + 1, right + 1):
        if A[j] < pivot:
            swap(A, j, i)
            i += 1
    swap(A, left, i - 1)
    return i

def _quicksort(A, left, right, choose_pivot):
    if left >= right: return
    global comparisons
    comparisons += right - left
    pivot_index = choose_pivot(A, left, right)
    i = partition(A, left, right, pivot_index)
    _quicksort(A, left, i - 2, choose_pivot)
    _quicksort(A, i, right, choose_pivot)

def quicksort(A, choose_pivot):
    _quicksort(A, 0, len(A) - 1, choose_pivot)

def read_file(filename):
    with open(filename) as f:
        return [int(line) for line in f]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute total number of comparisons used by QuickSort.")
    parser.add_argument('filename', type=str, help="file containing list of integers")
    
    args = parser.parse_args()
    
    integer_list = read_file(args.filename)
    rules = [choose_first, choose_last, choose_median]
    for rule in rules:
        comparisons = 0
        quicksort(integer_list[:], rule)
        print(rule.__name__ + ":", comparisons)