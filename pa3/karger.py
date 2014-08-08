#!/usr/bin/env python3

"""
Implementation of Karger's algorithm for computing a minimum cut of a connected graph.
"""

import argparse
import copy

class Vertex:
    def __init__(self, value):
        self.value = value
        self.parent = self
    def __eq__(self, that):
        return self.get_rep().value == that.get_rep().value
    def __hash__(self):
        return self.value
    def __repr__(self):
        return str(self.value)
    def get_rep(self):
        rep = self.parent
        while rep.value != rep.parent.value:
            rep = rep.parent
        return rep

class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
    def __eq__(self, that):
        return (self.u == that.u and self.v == that.v) or (self.u == that.v and self.v == that.u)
    def __repr__(self):
        return str(self.u.value) + "-" + str(self.v.value)

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.vertex_count = 0
    def parse_adjacency_lists(self, adjacency_lists):
        for adjacency_list in adjacency_lists:
            self.parse_adjacency_list(adjacency_list)
    def parse_adjacency_list(self, adjacency_list):
        vertex_value = adjacency_list[0]
        if vertex_value not in self.vertices.keys():
            vertex = Vertex(vertex_value)
            self.vertices[vertex_value] = vertex
            self.vertex_count += 1
        else:
            vertex = self.vertices[vertex_value]
        adjacency_list = adjacency_list[1:]
        for adjacent_vertex_value in adjacency_list:
            if adjacent_vertex_value not in self.vertices.keys():
                adjacent_vertex = Vertex(adjacent_vertex_value)
                self.vertices[adjacent_vertex_value] = adjacent_vertex
                self.vertex_count += 1
            else:
                adjacent_vertex = self.vertices[adjacent_vertex_value]
            edge = Edge(vertex, adjacent_vertex)
            if edge not in self.edges:
                self.edges.append(edge)
    def fuse(self, u, v):
        self.vertex_count -= 1
        u_rep = u.get_rep()
        v_rep = v.get_rep()
        if u_rep.value <= v_rep.value:
            v_rep.parent = u_rep
        else:
            u_rep.parent = v_rep
    def choose_random_edge(self):
        import random
        i = random.randrange(0, len(self.edges))
        random_edge = self.edges.pop(i)
        return random_edge
    def remove_self_loops(self):
        new_edges = []
        for edge in self.edges:
            if edge.u != edge.v:
                new_edges.append(edge)
        self.edges = new_edges[:]
    def contract(self):
        while self.vertex_count > 2:
            random_edge = self.choose_random_edge()
            self.fuse(random_edge.u, random_edge.v)
            self.remove_self_loops()
        return len(self.edges), self.edges

def parse_file(file_name):
    with open(file_name) as f:
        content = f.readlines()

    parsed_content = []

    for line in content:
        line = [int(i) for i in line.split()]
        parsed_content.append(line)

    return parsed_content

def karger(filename, verbose = False):
    adjacency_lists = parse_file(filename)

    min_cut_size = float("inf")
    min_cut = None

    original_graph = Graph()
    if verbose: print("Building graph...")
    original_graph.parse_adjacency_lists(adjacency_lists)

    if verbose: print("Running contractions...")
    for iteration in range(args.iterations):
        if verbose: print("Iteration:", iteration + 1)
        graph = copy.deepcopy(original_graph)
        cut_size, cut = graph.contract()
        if cut_size < min_cut_size:
            min_cut_size = cut_size
            min_cut = cut
    
    return min_cut_size, min_cut

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute minimum cut of a connected graph.")
    parser.add_argument('filename', type=str, help="file containing graph")
    parser.add_argument('iterations', metavar='iter', type=int, help="number of iterations to run")
    parser.add_argument('--verbose', action='store_true', help="print additional messages")
    
    args = parser.parse_args()

    min_cut_size, min_cut = karger(args.filename, args.verbose)

    print("Minimum cut size:", min_cut_size)
    print("Minimum cut:", min_cut)