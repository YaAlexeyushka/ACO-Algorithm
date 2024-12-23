from graph.algorithm.ACO import ACO
from graph.vertex.vertex import Vertex
import sys
sys.setrecursionlimit(1000000)


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, vertex1, vertex2, weight): 
        if vertex1 not in self.graph:
            v1 = Vertex(vertex1)
            self.graph[vertex1] = v1 
        if vertex2 not in self.graph:
            v2 = Vertex(vertex2)
            self.graph[vertex2] = v2
        
        self.graph[vertex1].add_neighbor(vertex2, weight)

    def display(self):
        for vertex in self.graph:
            edges_str = ', '.join([f"{neighbor} (вес {weight})" for neighbor, weight in self.graph[vertex].neighbors.items()])
            print(f"{vertex} -> {edges_str}")
    
    def get_accessible_vertices(self, vertex, way=[]):
        return [neighbor for neighbor in self.graph[vertex].get_neighbors() if neighbor not in way]

    def get_vertices(self):
        return list(self.graph.keys())

    def get_weight(self, vertex1, vertex2):
        return self.graph[vertex1].get_neighbor_weight(vertex2)

    def calculate_way_weight(self, way):
        weight = 0
        for i in range(len(way) - 1):
            edge_weight = self.get_weight(way[i], way[i + 1])
            if edge_weight is not None:
                weight += edge_weight
        return weight

    def calculate_ACO(self, iterat=100, ants=None, Q=4, p=1, first_vertex=None, show=True, log=True):
        alg = ACO(iterat, ants, Q, p, first_vertex, show, log)
        return alg.calc(self)

    def is_hamiltonian_cycle(self, path, pos, vertices):
        if pos == len(vertices):  
            return self.get_weight(path[pos - 1], path[0]) is not None

        for vertex in vertices:
            if vertex not in path and self.get_weight(path[pos - 1], vertex) is not None:
                path[pos] = vertex
                if self.is_hamiltonian_cycle(path, pos + 1, vertices):
                    return True
                path[pos] = None

        return False

    def has_hamiltonian_cycle(self):
        vertices = self.get_vertices()
        path = [None] * len(vertices)
        path[0] = vertices[0]
        return self.is_hamiltonian_cycle(path, 1, vertices)

    def make_hamiltonian(self):
        added_edges_amount = 0
        vertices = self.get_vertices()
        vertices_deg = {vertex: self.get_accessible_vertices(vertex) for vertex in vertices}
        vertices_deg = sorted(vertices_deg.items(), key=lambda item: len(item[1]))

        proper_deg = (len(vertices) + 1) // 4
        while True:
            for i in range(len(vertices_deg) - 1):
                if vertices_deg[i + 1][0] not in vertices_deg[0][1]:
                    self.add_edge(vertices_deg[0][0], vertices_deg[i + 1][0], 5)
                    added_edges_amount += 1
                    vertices_deg[0][1].append(vertices_deg[i + 1][0])
                    if vertices_deg[0][0] not in vertices_deg[i + 1][1]:
                        self.add_edge(vertices_deg[i + 1][0], vertices_deg[0][0], 5)
                        added_edges_amount += 1
                        vertices_deg[i + 1][1].append(vertices_deg[0][0])
                    break
            vertices_deg = sorted(vertices_deg, key=lambda item: len(item[1]))
            if len(vertices_deg[0][1]) >= proper_deg:
                return added_edges_amount

    # def extend_way(self, way, vertices, ways_edges, added_edges_amount, edge_weight, vertices_deg):
    #     while True:
    #         for vertex in vertices:
    #             if (way[-1], vertex) not in ways_edges and vertex not in way:
    #                 self.add_edge(way[-1], vertex, edge_weight)
    #                 ways_edges.add((way[-1], vertex))
    #                 added_edges_amount += 1
    #                 if way[-1] not in vertices_deg[vertex]:
    #                     ways_edges.add((vertex, way[-1]))
    #                     self.add_edge(vertex, way[-1], edge_weight)
    #                     added_edges_amount += 1
    #                 way.append(vertex)
    #                 break

    #         if len(way) == len(vertices):
    #             self.add_edge(way[-1], way[0], edge_weight)
    #             added_edges_amount += 1
    #             return added_edges_amount

    # def get_ways_edges(self, ways):
    #     ways_edges = set()
    #     for way in ways:
    #         for i in range(1, len(way)):
    #             ways_edges.add((way[i - 1], way[i]))
    #             ways_edges.add((way[i], way[i - 1]))
    #     return ways_edges

    # def get_way(self, vertices, way, vertex_number, vertices_deg, found_edges):
    #     for v in vertices:
    #         if v in self.graph[vertices[vertex_number]]:
    #             if (vertices[vertex_number], v) in found_edges:
    #                 continue
    #             found_edges.add((vertices[vertex_number], v))
    #             way.append(v)
    #             return self.get_way(vertices, way, vertex_number + 1, vertices_deg, found_edges)
    #     return way

    # def make_hamiltonian_alt(self, cycles_number=2, edge_weight=5):
    #     added_edges_amount = 0
    #     vertices = self.get_vertices()
    #     vertices_deg = {vertex: self.get_accessible_vertices(vertex) for vertex in vertices}

    #     found_edges = set()
    #     ways = []
    #     for v in vertices:
    #         ways.append(self.get_way(vertices, [v], 0, vertices_deg, found_edges))
    #     ways.sort(key=len, reverse=True)
    #     ways = ways[:cycles_number]

    #     ways_edges = self.get_ways_edges(ways)

    #     for way in ways:
    #         for i in range(1, len(way)):
    #             if way[i - 1] not in vertices_deg[way[i]]:
    #                 self.add_edge(way[i], way[i - 1], edge_weight)
    #                 added_edges_amount += 1
    #                 vertices_deg[way[i]].append(way[i - 1])

    #         added_edges_amount = self.extend_way(way, vertices, ways_edges,
    #                                              added_edges_amount, edge_weight,
    #                                              vertices_deg)

    #     return added_edges_amount
