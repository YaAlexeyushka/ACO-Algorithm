from graph.algorithm.ACO import ACO

class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.graph:
            self.add_vertex(vertex1)
        if vertex2 not in self.graph:
            self.add_vertex(vertex2)
            
        self.graph[vertex1].append([vertex2, weight])

    def display(self):
        for vertex, edges in self.graph.items():
            edges_str = ', '.join([f"{neighbor} (вес {weight})" for neighbor, weight in edges])
            print(f"{vertex} -> {edges_str}")
    
    def get_accessible_vertices(self, vertex):
        vertices = []
        for accessible_vertex in self.graph[vertex]:
            vertices.append(accessible_vertex[0])
        return vertices
    
    def get_vertices(self):
        vertices = []
        for vertex in self.graph:
            vertices.append(vertex)
        return vertices
    
    def get_weight(self, vertex1, vertex2):
        for accessible_vertex in self.graph[vertex1]:
            if accessible_vertex[0] == vertex2:
                weight = accessible_vertex[1]
                return weight       
                
    def calculate_way_weight(self, way):
        weight = 0
        for i in range(len(way)-1):
            weight += self.get_weight(way[i], way[i+1])
        return weight
    
    def calculate_ACO(self, iterat=100, ants=10, a=1, b=1, Q=4, p=1, show=True):
        alg = ACO(iterat, ants, a, b, Q, p, show)
        return alg.calc(self)
    



