#!/usr/bin/env python3

"""
Implementation of Dijkstra's algorithm for solving the single-source
shortest path problem for a graph with non-negative edges costs.
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
        return self.items[item.index // 2]
    def left_child(self, item):
        return self.items(2*item.index + 1)
    def right_child(self, item):
        return self.items(2*item.index + 2)
    def swap(self, this_item, that_item):
        temp_index = this_item.index
        this_item.index = that_item.index
        that_item.index = temp_index
        self.items[this_item.index] = this_item
        self.items[that_item.index] = that_item
    def bubble_up(self):
        assert(not self.is_empty())
        bubble = self.items[self.size - 1]
        while not self.is_root(bubble) and bubble < self.parent(bubble):
            self.swap(bubble, self.parent(bubble))
    def insert(self, key):
        item = Item(key, self.size)
        self.items.append(item)
        self.size += 1
        self.bubble_up()
    def bubble_down(self):
        bubble = self.items[0]
        while bubble > max(self.left_child(bubble), self.right_child(bubble)):
            self.swap(bubble, min(self.left_child(bubble)), self.right_child(bubble))
    def extract_min(self):
        min_item = self.items[0]
        self.items[0] = self.items.pop()
        self.size -= 1
        self.bubble_down()
        return min_item

class Edge:
    def __init__(self, tail, head, weight):
        self.tail = tail
        self.head = head
        self.weight = weight

class Graph:
    def __init__(self):
        self.n = 0
        self.vertices = set()
        self.tail_to_head = {}
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        self.tail_to_head[vertex] = set()
        self.n += 1
    def parse_file(self, filename):
        with open(filename) as f:
            content = f.readlines()

        for line in content:
            line = [i.split(',') for i in line.split()]
            vertex = int(line[0][0])
            vertex_adjacencies = []
            if vertex not in self.vertices:
                self.add_vertex(vertex)
            adjacencies = line[1:]
            for adjacency in adjacencies:
                vertex_adjacencies.append((int(adjacency[0]), int(adjacency[1])))
            self.tail_to_head[vertex] = vertex_adjacencies

def dijkstra(g, source):
    X = set([source])
    A = {}
    A[source] = 0
    while X != g.vertices:
        min_score = 1000000
        v_star = None
        w_star = None
        l_star = None
        for v in X:
            for adjacency in g.tail_to_head[v]:
                w = adjacency[0]
                weight = adjacency[1]
                if w not in X:
                    score = A[v] + weight
                    if score < min_score:
                        min_score = score
                        v_star = v
                        w_star = w
                        l_star = weight
        X.add(w_star)
        A[w_star] = A[v_star] + l_star
    return A

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute minimum cut of a connected graph.")
    parser.add_argument('filename', type=str, help="file containing graph")
    parser.add_argument('source', type=int, help="source vertex")
    parser.add_argument('destination', nargs='+', type=int, help="list of destination vertices")

    args = parser.parse_args()

    graph = Graph()
    graph.parse_file(args.filename)
    A = dijkstra(graph, args.source)
    print({vertex: A[vertex] for vertex in args.destination})
    