from graph.graph import Graph 
from graph.algorithm.ant.ant import Ant
from graph.algorithm.ACO import ACO
from graph.hamiltonian import make_hamiltonian, has_hamiltonian_cycle

import random
import time

g = Graph() 

graph_name = "graph.txt"
graph1000_name = "1000.txt"
with open(graph1000_name) as f:
    i = 0
    for edge in f:
        vertex1, vertex2, weight = edge.split()
        g.add_edge(vertex1, vertex2, int(weight))

print("Проверка на наличие гамильтонова цикла")
if_has_hamiltonian_cycle = has_hamiltonian_cycle(g)
if if_has_hamiltonian_cycle:
    print("Гамильтонов цикл существует")
else:
    print("Гамильтонов цикл не найден")
    
    print("Попытка создать в графе гамильтонов цикл")
    start_time = time.time()
    added_edges_amount = make_hamiltonian(g)
    calculating_time = time.time() - start_time
    print(f"Гамильтонов цикл создан за {calculating_time}; количество добавленных ребер: {added_edges_amount}")
        
    print("Проверка на наличие гамильтонова цикла")
    if_has_hamiltonian_cycle =  has_hamiltonian_cycle(g)
    if has_hamiltonian_cycle:
        print("Гамильтонов цикл существует")
    else:
        print("Гамильтонов цикл не найден")
        
if if_has_hamiltonian_cycle:
    ants = []
    for i in range(1):
        ants.append(Ant(1.2, 0.6))
        
    for i in range(0):
        ants.append(Ant(1.3, 0.7))
        
    print("запуск муравьев")
    
    # iterat = 3000
    # Q = 1
    # p = 0.1
    # first_vertex = None 
    # show = True 
    # log = True
    
    iterat = 200
    Q = 1
    p = 0
    first_vertex = 0
    show = True
    log = False
    
    start_time = time.time()
    alg = ACO(iterat, ants, Q, p, first_vertex, show, log)
    result = alg.calc(g)
    calculating_time = time.time() - start_time
    
    if result:
        print(f'найденный кратчайший путь: {result}, за время: {calculating_time}')
    else:
        print(F'алгоритм не нашел кратчайший путь {calculating_time}')


