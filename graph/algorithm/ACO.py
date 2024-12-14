import random
import copy
import matplotlib.pyplot as plt
from collections import Counter
import math
import numpy as np


class ACO:
    def __init__(self, _iterat=100,  _ants=10, _A=1, _B=1, _Q=4, _p=1, _show=True):
        self.iterat = _iterat
        self.ants = _ants
        self.A = _A
        self.B = _B
        self.Q = _Q 
        self.p = _p
        self.show = _show
        # self.MAX_PHEROMONE_AMOUNT = 120
        
        
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
                # accessible_vertex[-1] = min(accessible_vertex[-1], self.MAX_PHEROMONE_AMOUNT)
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
            product = (r**self.A) * (n**self.B)
            products.append(float(product))

        products_sum = sum(products)
        if products_sum == 0:
            return {}
        for i, accessible_vertex in enumerate(accessible_vertices):
            P = products[i] / products_sum
            if accessible_vertex not in accessible_vertices_attraction:
                accessible_vertices_attraction[accessible_vertex] = [P]
            else:
                accessible_vertices_attraction[accessible_vertex].append(P)
        
        return accessible_vertices_attraction
        
        
    def choose_vertex(self, accessible_vertices_attraction):
        # random_num = random.random()
        # sum = 0
        probabilities = []
        for v in accessible_vertices_attraction.values():
            probabilities.append(v[0])
        vertex = random.choices(list(accessible_vertices_attraction.keys()), probabilities)[0]
        # print(vertex)
        return vertex
        # for vertex in accessible_vertices_attraction:
        #     num = accessible_vertices_attraction[vertex][0]
        #     sum += num
        #     if random_num <= sum:
        #         return vertex
               
                
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
                return self.Q / worth
    
    
    def reduce_pheromone(self, pheromone_graph):
        for vertex in pheromone_graph:    
            for i, vertex2 in enumerate(pheromone_graph[vertex]):
                weight = vertex2[2]
                new_weight = (1-self.p)*weight
                # pheromone_graph[vertex][i][2] = new_weight
                if new_weight <= 1E-10:
                    new_weight = 0
                else:
                    pheromone_graph[vertex][i][2] = new_weight

    
    def choose_first_vertex(self, vertices):
        random_num = random.randint(0, len(vertices)-1)
        return vertices[random_num]
    
    
    def calc_best_ways_possibility(self, graph, best_ways, pheromone_graph):
        ways_possibility = 0
        for way in best_ways:
            temp_graph = copy.deepcopy(graph) 
            possibilities = []
            for i in range(len(way)-2):
                accessible_vertices_attraction = self.calculate_accessible_vertices_attraction(way[i], temp_graph, pheromone_graph)
                if not(accessible_vertices_attraction):
                    break
                possibility = accessible_vertices_attraction[way[i+1]][0]
                if possibility <= 1:
                    possibilities.append(accessible_vertices_attraction[way[i+1]][0])
                self.delete_vertex(way[i], temp_graph)
            # print(possibilities)
            products = math.prod(possibilities) / len(graph.get_vertices())
            ways_possibility += products
            # print(ways_possibility)
        if ways_possibility == 0:
            ways_possibility = None
        return ways_possibility
                
    
    def fill_history(self, best_ways_possibility_history):
        return [None] * (self.iterat - len(best_ways_possibility_history)) + best_ways_possibility_history
        # for i in range(len(result)):
        #     if result[i] == None:
        #         result[i] = 0
        # return result
        
    
    def get_avg_iter10_way_weights(self, iter_ways_weights):
        avg_iter10_way_weights = []
        way_weights = np.array([])
        for i in iter_ways_weights:
            way_weights = np.append(way_weights, iter_ways_weights[i])
            if i >= 9:
                avg_iter10_way_weights.append(np.mean(way_weights))
                way_weights = way_weights[1:]
        return avg_iter10_way_weights
            
                
    def calc_way_pheromone(self, best_ways, pheromone_graph):
        best_ways = list(best_ways)
        way_pheromone = 0
        if len(best_ways) == 0:
            return None
        for way in best_ways:
            for i in range(len(way)-1):
                way_pheromone += self.get_pheromone(way[i], way[i+1], pheromone_graph)
        return way_pheromone
              
                
    def calc(self, graph):
        best_ways = set()
        best_ways_possibility_history = []
        ways_weights = [1000000000000]
        iter_ways_weights = {}
        vertices = graph.get_vertices()
        optimal_way_pheromones_history = []
        
        pheromone_graph = self.get_pheromone_graph(graph, vertices)
        
        for i in range(self.iterat):
            first_vertex = self.choose_first_vertex(vertices)
            # print(f"Итерация {i}: Феромоны {pheromone_graph}")
            if self.show:
                best_ways_possibility = self.calc_best_ways_possibility(graph, best_ways, pheromone_graph)
                optimal_way_pheromones_history.append( self.calc_way_pheromone(best_ways, pheromone_graph) )
                
            temp_pheromone_graph = copy.deepcopy(pheromone_graph) 
            
            for ant in range(self.ants):
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
                    # way_possibilities.append(accessible_vertices_attraction[new_vertex][0])
                    pheromone_change = self.calculate_pheromone_change(vertex, new_vertex, pheromone_graph)
                    self.add_pheromone(vertex, new_vertex, pheromone_graph, pheromone_change)
                    self.delete_vertex(new_vertex, temp_graph)
                    vertex = new_vertex
                    way += f'{new_vertex}'  

                    # Возврат к первой вершине
                    is_last_vertex = v == len(vertices)-2
                    if (is_last_vertex):
                        pheromone_change = self.calculate_pheromone_change(new_vertex, first_vertex, pheromone_graph)
                        self.add_pheromone(vertex, new_vertex, pheromone_graph, pheromone_change)
                        if pheromone_change:
                            way += f'{first_vertex}'  
                        else:
                            is_way_proper = False
                            break
                
                if is_way_proper:
                    vertex_weight = graph.calculate_way_weight(way)
                    if not i in iter_ways_weights.keys():
                        iter_ways_weights[i] = [vertex_weight]
                    else:
                        iter_ways_weights[i].append(vertex_weight)
                        
                    if vertex_weight < min(ways_weights):
                        best_ways = set()
                        best_ways.add(way)
                        best_ways_possibility_history = []
                        optimal_way_pheromones_history = []
                    elif vertex_weight == min(ways_weights):
                        best_ways.add(way)
                    ways_weights.append(vertex_weight)
                    
            if self.show and best_ways_possibility:
                best_ways_possibility_history.append(best_ways_possibility)
            self.reduce_pheromone(pheromone_graph)
            
            # if (len(ways_weights) != 0):
            #     best_ways_weights.append( min(ways_weights ))
                        
        if self.show:
            best_ways_possibility_history = self.fill_history(best_ways_possibility_history)
            optimal_way_pheromones_history = self.fill_history(optimal_way_pheromones_history)
            avg_iter10_way_weights = self.get_avg_iter10_way_weights(iter_ways_weights)
            
            iterations1 = list(range(1, self.iterat + 1))
            iterations2 = list(range(10, len(avg_iter10_way_weights)+10))
            iterations3 = list(range(1, self.iterat + 1))
            
            fig, axs = plt.subplots(3, sharex = True)
            
            axs[0].plot(iterations1, best_ways_possibility_history)
            axs[0].set_title('Шанс пройти по оптимальному (одному из) пути')
            axs[0].grid()
            axs[0].set_xscale('log')
            
            axs[1].plot(iterations2, avg_iter10_way_weights)
            axs[1].set_title('Средний путь за каждые 10 итераций')
            axs[1].grid()
            axs[1].set_xscale('log')
            
            axs[2].plot(iterations3, optimal_way_pheromones_history)
            axs[2].set_title('Количество феромона на оптимальных путях')
            axs[2].grid()
            axs[2].set_xscale('log')
    
            plt.show()  
        
        if (len(ways_weights) != 0):
            result = min(ways_weights)
        else:
            result = None
        
        return result, list(best_ways)[0]









