from typing import Dict, List, Optional


class Vertex:
    """
    Класс Vertex представляет вершину графа с именем и списком соседей.

    Каждый сосед хранится в виде ключа (имя вершины), а значение — список, где
    первый элемент — вес ребра, а последующие могут хранить дополнительные данные,
    например, значение феромона.
    """

    def __init__(self, name: str) -> None:
        """
        Инициализирует вершину с заданным именем и пустым набором соседей.

        :param name: Имя вершины.
        """
        self.name: str = name
        self.neighbors: Dict[str, List[float]] = {}

    def add_neighbor(self, neighbor: str, weight: float) -> None:
        """
        Добавляет соседа с указанным весом ребра.

        Если сосед уже присутствует, его данные будут перезаписаны.

        :param neighbor: Имя соседней вершины.
        :param weight: Вес ребра к соседу.
        """
        self.neighbors[neighbor] = [weight]

    def get_neighbor_weight(self, neighbor: str) -> Optional[float]:
        """
        Возвращает вес ребра к указанной соседней вершине.

        :param neighbor: Имя соседней вершины.
        :return: Вес ребра, если сосед найден, иначе None.
        """
        if neighbor in self.neighbors:
            return self.neighbors[neighbor][0]
        return None

    def get_neighbors(self) -> List[str]:
        """
        Возвращает список имён соседних вершин.

        :return: Список имён соседей.
        """
        return list(self.neighbors.keys())
