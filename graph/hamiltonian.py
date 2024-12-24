from graph.graph import Graph 

def is_hamiltonian_cycle(graph, path, pos, vertices):
        if pos == len(vertices):  
            return graph.get_weight(path[pos - 1], path[0]) is not None

        for vertex in vertices:
            if vertex not in path and graph.get_weight(path[pos - 1], vertex) is not None:
                path[pos] = vertex
                if is_hamiltonian_cycle(graph, path, pos + 1, vertices):
                    return True
                path[pos] = None

        return False

def has_hamiltonian_cycle(graph):
    vertices = graph.get_vertices()
    path = [None] * len(vertices)
    path[0] = vertices[0]
    return is_hamiltonian_cycle(graph, path, 1, vertices)

def make_hamiltonian(graph):
    added_edges_amount = 0
    vertices = graph.get_vertices()
    vertices_deg = {vertex: graph.get_accessible_vertices(vertex) for vertex in vertices}
    vertices_deg = sorted(vertices_deg.items(), key=lambda item: len(item[1]))

    proper_deg = (len(vertices) + 1) // 4
    while True:
        for i in range(len(vertices_deg) - 1):
            if vertices_deg[i + 1][0] not in vertices_deg[0][1]:
                graph.add_edge(vertices_deg[0][0], vertices_deg[i + 1][0], 5)
                added_edges_amount += 1
                vertices_deg[0][1].append(vertices_deg[i + 1][0])
                if vertices_deg[0][0] not in vertices_deg[i + 1][1]:
                    graph.add_edge(vertices_deg[i + 1][0], vertices_deg[0][0], 5)
                    added_edges_amount += 1
                    vertices_deg[i + 1][1].append(vertices_deg[0][0])
                break
        vertices_deg = sorted(vertices_deg, key=lambda item: len(item[1]))
        if len(vertices_deg[0][1]) >= proper_deg:
            return added_edges_amount