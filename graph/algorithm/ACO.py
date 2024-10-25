import random
import copy
import matplotlib.pyplot as plt
from collections import Counter


class ACO:
    def __init__(self, _iterat=100,  _ants=10, _A=1, _B=1, _Q=4, _p=1, _show=True):
        self.iterat = _iterat
        self.ants = _ants
        self.A = _A
        self.B = _B
        self.Q = _Q 
        self.p = _p
        self.show = _show
        
        
    def get_pheromone_graph(self, graph, vertices):
        pheromone_graph = graph.graph
        for vertex in vertices:
            for accessible_vertex in pheromone_graph[vertex]:
                accessible_vertex.append(1)
        return pheromone_graph
        
                
    def get_pheromone(self, vertex1, vertex2, pheromone_graph):
        for accessible_vertex in pheromone_graph[vertex1]:
            if accessible_vertex[0] == vertex2:
                pheromone = accessible_vertex[-1]
                break
        return pheromone
    
    
    def add_pheromone(self, vertex1, vertex2, pheromone_graph, value):
        for accessible_vertex in pheromone_graph[vertex1]:
            if accessible_vertex[0] == vertex2:
                accessible_vertex[-1] += value
                break
        
        
    def calculate_n(self, graph, vertex1, vertex2):
        weight =  graph.get_weight(vertex1, vertex2)
        n = 1 / weight
        return n
    
                
    def calculate_accessible_vertices_attraction(self, vertex, graph, pheromone_graph):
        accessible_vertices_attraction = {}
        products = []
        accessible_vertices = graph.get_accessible_vertices(vertex)

        for accessible_vertex in accessible_vertices:
            r = self.get_pheromone(vertex, accessible_vertex, pheromone_graph)
            n = self.calculate_n(graph, vertex, accessible_vertex)
            product = r**self.A * n**self.B
            products.append(product)

        products_sum = sum(products)
        for i, accessible_vertex in enumerate(accessible_vertices):
            P = products[i] / products_sum
            if accessible_vertex not in accessible_vertices_attraction:
                accessible_vertices_attraction[accessible_vertex] = [P]
            else:
                accessible_vertices_attraction[accessible_vertex].append(P)
        
        return accessible_vertices_attraction
        
        
    def choose_vertex(self, accessible_vertices_attraction):
        random_num = random.random()
        sum = 0
        for vertex in accessible_vertices_attraction:
            num = accessible_vertices_attraction[vertex][0]
            sum += num
            if random_num <= sum:
                return vertex
               
                
    def delete_vertex(self, vertex, temp_graph):
        for i in temp_graph.graph:
            for j, arr in enumerate(temp_graph.graph[i]):
                if arr[0] == vertex:
                    temp_graph.graph[i].pop(j)
                    break
                
                
    def calculate_pheromone_change(self, vertex1, vertex2, pheromone_graph):
        for vertex in pheromone_graph[vertex1]:
            if vertex[0] == vertex2:
                worth = vertex[1]
                return 1 / worth
    
    
    def choose_first_vertex(self, vertices):
        random_num = random.randint(0, len(vertices)-1)
        return vertices[random_num]
    
                
    def calc(self, graph):
        best_way = None
        ways = []
        ways_weights = []
        best_ways_weights = []
        vertices = graph.get_vertices()
        pheromone_graph = self.get_pheromone_graph(graph, vertices)
                
        for i in range(self.iterat):
            temp_pheromone_graph = copy.deepcopy(pheromone_graph) 
            
            for ant in range(self.ants):
                first_vertex = self.choose_first_vertex(vertices)
                vertex = first_vertex  
                is_way_proper = True
                way = f'{first_vertex}'  
                temp_graph = copy.deepcopy(graph)
                self.delete_vertex(first_vertex, temp_graph)
                
                for v in range(len(vertices)-1):
                    accessible_vertices_attraction = self.calculate_accessible_vertices_attraction(vertex, temp_graph, temp_pheromone_graph)
                    if not accessible_vertices_attraction:
                        is_way_proper = False
                        break
                    new_vertex = self.choose_vertex(accessible_vertices_attraction)
                    pheromone_change = self.calculate_pheromone_change(vertex, new_vertex, pheromone_graph)
                    self.add_pheromone(vertex, new_vertex, pheromone_graph, pheromone_change)
                    self.delete_vertex(new_vertex, temp_graph)
                    vertex = new_vertex
                    way += f'{new_vertex}'  

                    # Возврат к первой вершине
                    is_last_vertex = v == len(vertices)-2
                    if (is_last_vertex):
                        pheromone_change = self.calculate_pheromone_change(new_vertex, first_vertex, pheromone_graph)
                        if pheromone_change:
                            way += f'{first_vertex}'  
                        else:
                            is_way_proper = False
                            break
                
                if is_way_proper:
                    vertex_weight = graph.calculate_way_weight(way)
                    ways_weights.append( vertex_weight  )
                    if vertex_weight <= min(ways_weights):
                        best_way = way
            
            if (len(ways_weights) != 0):
                best_ways_weights.append( min(ways_weights ))
        
        if self.show:
            plt.grid()
            plt.plot(range(1, len(best_ways_weights) + 1), best_ways_weights)
            plt.xlabel('Итерация')
            plt.ylabel('Вес лучшего пути')
            plt.show()
        
        return min(best_ways_weights), best_way









