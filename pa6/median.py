#!/usr/bin/env python3

"""
Implementation of a median maintenance algorithm using two heaps.
This algorithm efficiently keeps track of the median of a stream of integers.
"""

import argparse

class Item:
    def __init__(self, key, index = None):
        self.key = key
        self.index = index
    def __eq__(self, that):
        return self.key == that.key
    def __lt__(self, that):
        return self.key < that.key
    def __le__(self, that):
        return self.key <= that.key
    def __repr__(self):
        return str(self.key)

class Heap:
    def __init__(self):
        self.items = []
        self.size = 0
    def is_empty(self):
        return self.size == 0
    def is_root(self, item):
        return item.index == 0
    def parent(self, item):
        if item.index == 0:
            return None
        return self.items[(item.index - 1) // 2]
    def has_left_child(self, item):
        return 2*item.index + 1 < self.size
    def has_right_child(self, item):
        return 2*item.index + 2 < self.size
    def is_leaf(self, item):
        return not self.has_left_child(item) and not self.has_right_child(item)
    def left_child(self, item):
        child_index = 2*item.index + 1
        if child_index >= self.size:
            return None
        return self.items[child_index]
    def right_child(self, item):
        child_index = 2*item.index + 2
        if child_index >= self.size:
            return None
        return self.items[child_index]
    def swap(self, this_item, that_item):
        temp_index = this_item.index
        this_item.index = that_item.index
        that_item.index = temp_index
        self.items[this_item.index] = this_item
        self.items[that_item.index] = that_item
    def insert_key(self, key):
        item = Item(key, self.size)
        self.items.append(item)
        self.size += 1
        self.bubble_up()
    def insert_item(self, item):
        item.index = self.size
        self.items.append(item)
        self.size += 1
        self.bubble_up()
    def get_root(self):
        assert(not self.is_empty())
        return self.items[0]
    def extract_root(self):
        item = self.items[0]
        self.items[0] = self.items.pop()
        self.items[0].index = 0
        self.size -= 1
        self.bubble_down()
        return item
    def check(self):
        for i in range(self.size):
            assert(i == self.items[i].index)

class MinHeap(Heap):
    def bubble_up(self):
        assert(not self.is_empty())
        bubble = self.items[self.size - 1]
        while not self.is_root(bubble) and bubble < self.parent(bubble):
            self.swap(bubble, self.parent(bubble))
    def bubble_down(self):
        bubble = self.items[0]
        while not self.is_leaf(bubble):
            smaller_child = self.left_child(bubble)
            if self.has_right_child(bubble) and self.right_child(bubble) < smaller_child:
                smaller_child = self.right_child(bubble)
            if bubble <= smaller_child:
                break
            self.swap(bubble, smaller_child)
    def get_min(self):
        return self.get_root()
    def extract_min(self):
        return self.extract_root()

class MaxHeap(Heap):
    def bubble_up(self):
        assert(not self.is_empty())
        bubble = self.items[self.size - 1]
        while not self.is_root(bubble) and bubble > self.parent(bubble):
            self.swap(bubble, self.parent(bubble))
    def bubble_down(self):
        bubble = self.items[0]
        while not self.is_leaf(bubble):
            bigger_child = self.left_child(bubble)
            if self.has_right_child(bubble) and self.right_child(bubble) > bigger_child:
                bigger_child = self.right_child(bubble)
            if bubble >= bigger_child:
                break
            self.swap(bubble, bigger_child)
    def get_max(self):
        return self.get_root()
    def extract_max(self):
        return self.extract_root()
        
class MedianMaintenance:
    def __init__(self):
        self.small_heap = MaxHeap()
        self.large_heap = MinHeap()
    def rebalance(self):
        if self.small_heap.size > self.large_heap.size + 1:
            item = self.small_heap.extract_root()
            self.large_heap.insert_item(item)
        elif self.large_heap.size > self.small_heap.size + 1:
            item = self.large_heap.extract_root()
            self.small_heap.insert_item(item)
    def insert_key(self, key):
        item = Item(key)
        if self.small_heap.size == 0 or item <= self.get_median():
            self.small_heap.insert_item(item)
        else:
            self.large_heap.insert_item(item)
        self.rebalance()
    def get_median(self):
        if self.small_heap.size >= self.large_heap.size:
            return self.small_heap.get_root()
        else:
            return self.large_heap.get_root()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keep track of the median of a stream of integers")
    parser.add_argument('filename', type=str, help="file containing integers")
    
    args = parser.parse_args()

    with open(args.filename) as f:
        content = list(f)

    m = MedianMaintenance()
    medians_sum = 0

    for line in content:
        m.insert_key(int(line))
        median = m.get_median()
        medians_sum += median.key

    print(medians_sum)