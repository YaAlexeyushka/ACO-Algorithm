import random
import copy
import matplotlib.pyplot as plt
from collections import Counter
import math
import numpy as np


class ACO:
    def __init__(self, _iterat=100,  _ants=None, _Q=4, _p=1, _first_vertex=None, _show=True, _log=True):
        self.iterat = _iterat
        self.ants = _ants
        self.Q = _Q 
        self.p = _p
        self.first_vertex = _first_vertex
        self.show = _show
        self.log = _log
        
        
    def make_pheromone_graph(self, graph):
        for vertex in graph.graph:
            for vertex2 in graph.graph[vertex].get_neighbors():
                graph.graph[vertex].neighbors[vertex2].append(1)
                
                
    def get_pheromone(self, vertex1, vertex2, graph):
        return graph.graph[vertex1].neighbors[vertex2][1]
                
                
    def add_pheromone(self, ways, graph):
        for way in ways:
            for i in range(len(way)-1):
                pheromone_change = self.calculate_pheromone_change(way[i], way[i+1], graph)
                graph.graph[way[i]].neighbors[way[i+1]][1] += pheromone_change        
        
    def calculate_n(self, graph, vertex1, vertex2):
        weight =  graph.get_weight(vertex1, vertex2)
        n = 1 / weight
        return n
    
                
    def calculate_accessible_vertices_attraction(self, ant, vertex, graph, way):
        accessible_vertices_attraction = {}
        products = []
        products_sum = 0
        accessible_vertices = graph.get_accessible_vertices(vertex, way)

        for accessible_vertex in accessible_vertices:
            r = self.get_pheromone(vertex, accessible_vertex, graph)
            n = self.calculate_n(graph, vertex, accessible_vertex)
            product = (r**ant.A) * (n**ant.B)
            products.append(product)
            products_sum += product

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
        random_num = random.random()
        sum = 0
        for vertex in accessible_vertices_attraction:
            num = accessible_vertices_attraction[vertex][0]
            sum += num
            if random_num <= sum:
                return vertex
                
                
    def calculate_pheromone_change(self, vertex1, vertex2, graph):
        if vertex2 in graph.graph[vertex1].get_neighbors():
            weight = graph.get_weight(vertex1, vertex2)
            return self.Q / weight
    
    
    def reduce_pheromone(self, graph):
        for vertex1 in graph.graph:    
            for vertex2 in graph.graph[vertex1].get_neighbors():
                graph.graph[vertex1].neighbors[vertex2][1] *= (1-self.p)

    
    def choose_first_vertex(self, vertices):
        random_num = random.randint(0, len(vertices)-1)
        return vertices[random_num]
    
    
    def calc_best_ways_possibility(self, graph, best_ways):
        ways_possibility = 0
        for way in best_ways:
            possibilities = []
            current_way = []
            for i in range(len(way)-2):
                current_way.append(way[i])
                accessible_vertices_attraction = self.calculate_accessible_vertices_attraction(self.ants[0], way[i],
                                                                                               graph, current_way)
                if not(accessible_vertices_attraction):
                    break
                possibilities.append(accessible_vertices_attraction[way[i+1]][0])
            products = math.prod(possibilities)
            if self.first_vertex == None:
                products /= len(graph.get_vertices())
            ways_possibility += products
        if ways_possibility == 0:
            ways_possibility = None
        return ways_possibility
                
    
    def fill_history(self, best_ways_possibility_history):
        return [None] * (self.iterat - len(best_ways_possibility_history)) + best_ways_possibility_history
        
    
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
        
        if self.first_vertex != None:
            first_vertex = vertices[self.first_vertex]
        
        self.make_pheromone_graph(graph)
        
        for i in range(self.iterat):
            iter_ways = []
            if self.first_vertex == None:
                first_vertex = self.choose_first_vertex(vertices)
            if self.show:
                best_ways_possibility = self.calc_best_ways_possibility(graph, best_ways)
                optimal_way_pheromones_history.append(self.calc_way_pheromone(best_ways, graph))
                
            
            for ant in self.ants:
                vertex = first_vertex  
                is_way_proper = True
                way = [first_vertex]
                
                for v in range(len(vertices)-1):
                    accessible_vertices_attraction = self.calculate_accessible_vertices_attraction(ant, vertex,
                                                                                                   graph, way)
                    if not accessible_vertices_attraction:
                        is_way_proper = False
                        break
                    new_vertex = self.choose_vertex(accessible_vertices_attraction)
                    vertex = new_vertex
                    way.append(new_vertex) 

                    # Возврат к первой вершине
                    is_last_vertex = v == len(vertices)-2
                    if (is_last_vertex):
                        pheromone_change = self.calculate_pheromone_change(new_vertex, first_vertex, graph)
                        if pheromone_change:
                            way.append(first_vertex)
                        else:
                            is_way_proper = False
                            break
                
                if is_way_proper:
                    iter_ways.append(way)
                    way_weight = graph.calculate_way_weight(way)
                    if not i in iter_ways_weights.keys():
                        iter_ways_weights[i] = [way_weight]
                    else:
                        iter_ways_weights[i].append(way_weight)
                        
                    if way_weight < min(ways_weights):
                        best_ways = set()
                        best_ways.add(tuple(way))
                        best_ways_possibility_history = []
                        optimal_way_pheromones_history = []
                    elif way_weight == min(ways_weights):
                        best_ways.add(tuple(way))
                    ways_weights.append(way_weight)
            
            if self.show and best_ways_possibility:
                best_ways_possibility_history.append(best_ways_possibility)
                
            if self.p > 0:
                self.reduce_pheromone(graph)
            self.add_pheromone(iter_ways, graph)  
                        
        if self.show:
            best_ways_possibility_history = self.fill_history(best_ways_possibility_history)
            optimal_way_pheromones_history = self.fill_history(optimal_way_pheromones_history)
            avg_iter10_way_weights = self.get_avg_iter10_way_weights(iter_ways_weights)
            
            iterations1 = list(range(1, self.iterat + 1))
            iterations2 = list(range(10, len(avg_iter10_way_weights)+10))
            iterations3 = list(range(1, self.iterat + 1))
            
            fig, axs = plt.subplots(3, sharex = True)
            
            axs[0].plot(iterations1, best_ways_possibility_history)
            axs[0].set_title('Шанс пройти по оптимальным путям')
            axs[0].grid()
            
            axs[1].plot(iterations2, avg_iter10_way_weights)
            axs[1].set_title('Средний путь за каждые 10 итераций')
            axs[1].grid()
            
            axs[2].plot(iterations3, optimal_way_pheromones_history)
            axs[2].set_title('Количество феромона на оптимальных путях')
            axs[2].grid()

            if self.log == True:
                axs[0].set_xscale('log')
                axs[1].set_xscale('log')
                axs[2].set_xscale('log')
                
            plt.show()  
        
        if (len(ways_weights) != 0):
            result = min(ways_weights)
        else:
            return None
        
        if best_ways:
            return result, list(best_ways)[0]
        else:
            return None









