from graph.graph import Graph 
import random
import time

g1 = Graph()
g1.add_edge('d', 'c', 8)
g1.add_edge('a', 'f', 1)
g1.add_edge('c', 'b', 3)
g1.add_edge('b', 'a', 3)
g1.add_edge('a', 'b', 3)
g1.add_edge('b', 'c', 8)
g1.add_edge('b', 'g', 3)
g1.add_edge('c', 'g', 1)
g1.add_edge('c', 'd', 1)
g1.add_edge('g', 'b', 3)
g1.add_edge('d', 'f', 1)
g1.add_edge('f', 'd', 3)
g1.add_edge('g', 'a', 3)
g1.add_edge('f', 'a', 3)
g1.add_edge('g', 'c', 3)
g1.add_edge('g', 'd', 5)
g1.add_edge('g', 'f', 4)

g1.display()

# g = Graph() 
# with open("1000.txt") as f:
#     i = 0
#     for edge in f:
#         if edge[0].isdigit():
#             vertex1, vertex2, weight = edge.split()
#             g.add_edge(vertex1, vertex2, int(weight))

start_time = time.time()
result = g1.calculate_ACO(iterat = 1000, ants=3, a=1.2, b=0.6, Q=1, p=0.1, show=True)
calculating_time = time.time() - start_time
print(f'найденный кратчайший путь: {result}, за время: {calculating_time}')



