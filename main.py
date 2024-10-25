from graph.graph import Graph

g = Graph()
g.add_edge('A', 'B', 3)
g.add_edge('A', 'F', 1)
g.add_edge('B', 'A', 3)
g.add_edge('B', 'G', 3)
g.add_edge('B', 'C', 8)
g.add_edge('C', 'B', 3)
g.add_edge('C', 'G', 1)
g.add_edge('C', 'D', 1)
g.add_edge('D', 'C', 8)
g.add_edge('D', 'F', 1)
g.add_edge('F', 'A', 3)
g.add_edge('F', 'D', 3)
g.add_edge('G', 'A', 3)
g.add_edge('G', 'B', 3)
g.add_edge('G', 'C', 3)
g.add_edge('G', 'D', 5)
g.add_edge('G', 'F', 4)
        
result = g.calculate_ACO(iterat=100, ants=10, a=2, b=3, Q=5, p=0.5)
print(f'найденный кратчайший путь: {result}')

