from typing import List, Any
from graph.graph import Graph


def _is_hamiltonian_cycle(
    graph: Graph, path: List[Any], pos: int, vertices: List[Any]
) -> bool:
    """
    Рекурсивная функция для проверки, является ли текущий путь гамильтоновым циклом.

    :param graph: Объект графа.
    :param path: Текущий путь обхода вершин.
    :param pos: Текущая позиция в пути.
    :param vertices: Список всех вершин графа.
    :return: True, если найден гамильтонов цикл, иначе False.
    """
    # Если все вершины включены в путь, проверяем замыкание цикла.
    if pos == len(vertices):
        return graph.get_weight(path[pos - 1], path[0]) is not None

    # Проходим по всем вершинам, не включённым в путь
    for vertex in vertices:
        if vertex not in path and graph.get_weight(path[pos - 1], vertex) is not None:
            path[pos] = vertex
            if _is_hamiltonian_cycle(graph, path, pos + 1, vertices):
                return True
            path[pos] = None  # откат выбора

    return False


def has_hamiltonian_cycle(graph: Graph) -> bool:
    """
    Проверяет, содержит ли граф гамильтонов цикл.

    :param graph: Объект графа.
    :return: True, если гамильтонов цикл найден, иначе False.
    """
    vertices = graph.get_vertices()
    if not vertices:
        return False

    path: List[Any] = [None] * len(vertices)
    path[0] = vertices[0]
    return _is_hamiltonian_cycle(graph, path, 1, vertices)


def make_hamiltonian(graph: Graph) -> int:
    """
    Добавляет ребра в граф, чтобы гарантировать существование гамильтонова цикла.

    Алгоритм работает следующим образом:
      1. Выбирает вершины с минимальным числом смежных вершин.
      2. Если между наименее связанными вершинами отсутствует ребро, оно добавляется.
      3. Обновляется список смежных вершин и производится повторная сортировка.
      4. Операция завершается, когда у вершины с минимальным числом смежностей
         степень достигает заданного порогового значения.

    :param graph: Объект графа.
    :return: Количество добавленных ребер.
    """
    added_edges_amount = 0
    vertices = graph.get_vertices()

    # Формируем словарь, где ключ — вершина, значение — список достижимых вершин.
    vertex_neighbors = {
        vertex: graph.get_accessible_vertices(vertex) for vertex in vertices
    }
    # Сортируем вершины по количеству соседей
    sorted_vertices = sorted(vertex_neighbors.items(), key=lambda item: len(item[1]))

    # Определяем минимально необходимое количество соседей для вершины
    proper_degree = (len(vertices) + 1) // 4

    while True:
        # Ищем пару: наименее связанная вершина и другая вершина, с которой отсутствует связь.
        for i in range(len(sorted_vertices) - 1):
            vertex_a, neighbors_a = sorted_vertices[0]
            vertex_b, neighbors_b = sorted_vertices[i + 1]
            if vertex_b not in neighbors_a:
                # Добавляем ребро от vertex_a к vertex_b
                graph.add_edge(vertex_a, vertex_b, 5)
                added_edges_amount += 1
                neighbors_a.append(vertex_b)
                # Добавляем обратное ребро, если его ещё нет
                if vertex_a not in neighbors_b:
                    graph.add_edge(vertex_b, vertex_a, 5)
                    added_edges_amount += 1
                    neighbors_b.append(vertex_a)
                break

        # Обновляем сортировку по текущему количеству соседей
        sorted_vertices = sorted(
            vertex_neighbors.items(), key=lambda item: len(item[1])
        )
        # Если минимальная степень достигла порога, завершаем работу
        if len(sorted_vertices[0][1]) >= proper_degree:
            return added_edges_amount
