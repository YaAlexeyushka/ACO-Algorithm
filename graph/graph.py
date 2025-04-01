from graph.algorithm.ACO import ACO
from graph.vertex.vertex import Vertex
import sys
from typing import Dict, List, Optional, Union

sys.setrecursionlimit(1000000)


class Graph:
    """
    Класс Graph представляет граф, где вершины хранятся в виде объектов класса Vertex.
    """

    def __init__(self) -> None:
        # Словарь, где ключ — имя вершины, а значение — объект Vertex.
        self.vertices: Dict[str, Vertex] = {}

    def add_edge(self, vertex1: str, vertex2: str, weight: int) -> None:
        """
        Добавляет ребро между вершинами `vertex1` и `vertex2` с указанным весом.

        Если одна из вершин отсутствует, она будет создана.
        """
        if vertex1 not in self.vertices:
            self.vertices[vertex1] = Vertex(vertex1)
        if vertex2 not in self.vertices:
            self.vertices[vertex2] = Vertex(vertex2)
        self.vertices[vertex1].add_neighbor(vertex2, weight)

    def display(self) -> None:
        """
        Выводит представление графа: для каждой вершины отображает список смежных вершин и вес ребра.
        """
        for vertex, vertex_obj in self.vertices.items():
            edges_str = ", ".join(
                [
                    f"{neighbor} (вес {weight})"
                    for neighbor, weight in vertex_obj.neighbors.items()
                ]
            )
            print(f"{vertex} -> {edges_str}")

    def get_accessible_vertices(
        self, vertex: str, way: Optional[List[str]] = None
    ) -> List[str]:
        """
        Возвращает список доступных (смежных) вершин для заданной вершины,
        исключая те, что уже содержатся в списке `way`.

        :param vertex: Имя исходной вершины.
        :param way: Список вершин, которые необходимо исключить.
        :return: Список имён доступных вершин.
        """
        if way is None:
            way = []
        return [
            neighbor
            for neighbor in self.vertices[vertex].get_neighbors()
            if neighbor not in way
        ]

    def get_vertices(self) -> List[str]:
        """
        Возвращает список всех вершин графа.

        :return: Список имён вершин.
        """
        return list(self.vertices.keys())

    def get_weight(self, vertex1: str, vertex2: str) -> Optional[int]:
        """
        Возвращает вес ребра между вершинами `vertex1` и `vertex2`,
        либо None, если ребро отсутствует.

        :param vertex1: Имя исходной вершины.
        :param vertex2: Имя целевой вершины.
        :return: Вес ребра или None.
        """
        return self.vertices[vertex1].get_neighbor_weight(vertex2)

    def calculate_way_weight(self, way: List[str]) -> int:
        """
        Вычисляет суммарный вес пути, заданного списком имён вершин.

        :param way: Список вершин, образующих путь.
        :return: Общий вес пути.
        """
        total_weight = 0
        for i in range(len(way) - 1):
            edge_weight = self.get_weight(way[i], way[i + 1])
            if edge_weight is not None:
                total_weight += edge_weight
        return total_weight
