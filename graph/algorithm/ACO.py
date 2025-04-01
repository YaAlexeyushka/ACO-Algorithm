import random
import math
import copy
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from typing import Any, Dict, List, Optional, Set, Tuple


class ACO:
    """
    Класс для решения задачи коммивояжёра методом муравьиной колонии (Ant Colony Optimization).
    """

    def __init__(
        self,
        iterations: int = 100,
        ants: Optional[List[Any]] = None,
        Q: float = 4,
        evaporation_rate: float = 1,
        first_vertex_index: Optional[int] = None,
        show_plots: bool = True,
        log_scale: bool = True,
    ) -> None:
        """
        Инициализация параметров алгоритма ACO.

        :param iterations: Количество итераций алгоритма.
        :param ants: Список объектов-муравьёв, каждый из которых должен иметь атрибуты A и B.
        :param Q: Параметр, влияющий на изменение феромона.
        :param evaporation_rate: Коэффициент испарения феромона (значение p).
        :param first_vertex_index: Индекс стартовой вершины (если None — выбирается случайно).
        :param show_plots: Флаг для отображения графиков динамики алгоритма.
        :param log_scale: Флаг для отображения оси x в логарифмическом масштабе.
        """
        self.iterations = iterations
        self.ants = ants
        self.Q = Q
        self.evaporation_rate = evaporation_rate
        self.first_vertex_index = first_vertex_index
        self.show_plots = show_plots
        self.log_scale = log_scale

    def initialize_pheromones(self, graph: Any) -> None:
        """
        Инициализирует граф феромонов: для каждого ребра добавляет начальное значение феромона (1).

        :param graph: Объект графа с атрибутом graph (словарь вершин).
        """
        for vertex in graph.graph:
            for neighbor in graph.graph[vertex].get_neighbors():
                # Предполагается, что graph.graph[vertex].neighbors[neighbor] — это список,
                # где индекс 1 хранит значение феромона.
                graph.graph[vertex].neighbors[neighbor].append(1)

    def get_pheromone(self, vertex1: Any, vertex2: Any, graph: Any) -> float:
        """
        Возвращает значение феромона на ребре между vertex1 и vertex2.

        :param vertex1: Исходная вершина.
        :param vertex2: Целевая вершина.
        :param graph: Объект графа.
        :return: Значение феромона.
        """
        return graph.graph[vertex1].neighbors[vertex2][1]

    def add_pheromones(self, paths: List[List[Any]], graph: Any) -> None:
        """
        Обновляет значения феромона, добавляя изменение феромона для каждого ребра в каждом найденном пути.

        :param paths: Список найденных путей (каждый путь — список вершин).
        :param graph: Объект графа.
        """
        for path in paths:
            for i in range(len(path) - 1):
                delta_pheromone = self.calculate_pheromone_change(
                    path[i], path[i + 1], graph
                )
                graph.graph[path[i]].neighbors[path[i + 1]][1] += delta_pheromone

    def calculate_desirability(self, graph: Any, vertex1: Any, vertex2: Any) -> float:
        """
        Вычисляет меру привлекательности (desirability) перехода от vertex1 к vertex2,
        как обратную величину веса ребра.

        :param graph: Объект графа.
        :param vertex1: Исходная вершина.
        :param vertex2: Целевая вершина.
        :return: Значение привлекательности.
        """
        weight = graph.get_weight(vertex1, vertex2)
        return 1 / weight

    def calculate_accessible_attraction(
        self, ant: Any, current_vertex: Any, graph: Any, current_path: List[Any]
    ) -> Dict[Any, float]:
        """
        Вычисляет вероятность перехода для каждой доступной вершины, основываясь на феромоне и привлекательности.

        :param ant: Объект-муравей с атрибутами A и B.
        :param current_vertex: Текущая вершина.
        :param graph: Объект графа.
        :param current_path: Текущий построенный путь.
        :return: Словарь, где ключ — доступная вершина, значение — вероятность перехода.
        """
        probabilities: Dict[Any, float] = {}
        total_product = 0.0
        accessible_vertices = graph.get_accessible_vertices(
            current_vertex, current_path
        )

        # Вычисление произведения (r^A * n^B) для каждой доступной вершины.
        for neighbor in accessible_vertices:
            pheromone = self.get_pheromone(current_vertex, neighbor, graph)
            desirability = self.calculate_desirability(graph, current_vertex, neighbor)
            product = (pheromone**ant.A) * (desirability**ant.B)
            probabilities[neighbor] = product
            total_product += product

        if total_product == 0:
            return {}

        # Нормализация вероятностей.
        for neighbor in probabilities:
            probabilities[neighbor] /= total_product

        return probabilities

    def choose_next_vertex(self, probabilities: Dict[Any, float]) -> Optional[Any]:
        """
        Выбирает следующую вершину на основе рассчитанных вероятностей.

        :param probabilities: Словарь вероятностей перехода.
        :return: Выбранная вершина или None, если словарь пуст.
        """
        rand_val = random.random()
        cumulative = 0.0
        for vertex, prob in probabilities.items():
            cumulative += prob
            if rand_val <= cumulative:
                return vertex
        return None

    def calculate_pheromone_change(
        self, vertex1: Any, vertex2: Any, graph: Any
    ) -> Optional[float]:
        """
        Вычисляет изменение феромона для ребра между vertex1 и vertex2.

        :param vertex1: Исходная вершина.
        :param vertex2: Целевая вершина.
        :param graph: Объект графа.
        :return: Изменение феромона или None, если ребро отсутствует.
        """
        if vertex2 in graph.graph[vertex1].get_neighbors():
            weight = graph.get_weight(vertex1, vertex2)
            return self.Q / weight
        return None

    def reduce_pheromones(self, graph: Any) -> None:
        """
        Применяет процесс испарения феромона ко всем ребрам графа.

        :param graph: Объект графа.
        """
        for vertex in graph.graph:
            for neighbor in graph.graph[vertex].get_neighbors():
                graph.graph[vertex].neighbors[neighbor][1] *= 1 - self.evaporation_rate

    def choose_start_vertex(self, vertices: List[Any]) -> Any:
        """
        Случайным образом выбирает стартовую вершину из списка.

        :param vertices: Список вершин.
        :return: Выбранная вершина.
        """
        return vertices[random.randint(0, len(vertices) - 1)]

    def calculate_best_paths_probability(
        self, graph: Any, best_paths: Set[Tuple[Any, ...]]
    ) -> Optional[float]:
        """
        Вычисляет суммарную вероятность (шанс) прохождения оптимальных путей.

        :param graph: Объект графа.
        :param best_paths: Множество оптимальных путей (каждый путь — кортеж вершин).
        :return: Суммарная вероятность или None, если она равна 0.
        """
        total_probability = 0.0

        for path in best_paths:
            path_probability = 1.0
            current_path: List[Any] = []
            # Проходим по всем промежуточным вершинам, кроме последних двух.
            for i in range(len(path) - 2):
                current_path.append(path[i])
                attractions = self.calculate_accessible_attraction(
                    self.ants[0], path[i], graph, current_path
                )
                if not attractions:
                    path_probability = 0
                    break
                # Используем вероятность перехода к следующей вершине.
                path_probability *= attractions.get(path[i + 1], 0)
            if path_probability and self.first_vertex_index is None:
                path_probability /= len(graph.get_vertices())
            total_probability += path_probability

        return total_probability if total_probability != 0 else None

    def fill_history(self, history: List[Any]) -> List[Any]:
        """
        Дополняет историю значениями None спереди так, чтобы длина списка стала равна количеству итераций.

        :param history: Список значений истории.
        :return: Дополненный список.
        """
        return [None] * (self.iterations - len(history)) + history

    def get_avg_weight_per_10_iterations(
        self, iter_weights: Dict[int, List[float]]
    ) -> List[float]:
        """
        Вычисляет скользящее среднее значений веса пути за каждые 10 итераций.

        :param iter_weights: Словарь, где ключ — номер итерации, значение — список весов путей.
        :return: Список средних значений для каждых 10 итераций.
        """
        avg_weights: List[float] = []
        window: List[float] = []
        for i in sorted(iter_weights.keys()):
            window.extend(iter_weights[i])
            if i >= 9:
                avg_weights.append(np.mean(window))
                window = window[1:]
        return avg_weights

    def calculate_total_pheromone(
        self, best_paths: Set[Tuple[Any, ...]], graph: Any
    ) -> Optional[float]:
        """
        Вычисляет суммарное количество феромона на ребрах, входящих в оптимальные пути.

        :param best_paths: Множество оптимальных путей.
        :param graph: Объект графа.
        :return: Суммарное количество феромона или None, если путей нет.
        """
        total_pheromone = 0.0
        if not best_paths:
            return None
        for path in best_paths:
            for i in range(len(path) - 1):
                total_pheromone += self.get_pheromone(path[i], path[i + 1], graph)
        return total_pheromone

    def run(self, graph: Any) -> Optional[Tuple[float, Tuple[Any, ...]]]:
        """
        Основной метод выполнения алгоритма ACO.

        :param graph: Объект графа.
        :return: Кортеж (минимальный вес пути, оптимальный путь) или None.
        """
        best_paths: Set[Tuple[Any, ...]] = set()
        best_paths_probability_history: List[Any] = []
        path_weights: List[float] = [1e12]  # Начальное большое значение
        iter_weights: Dict[int, List[float]] = {}
        vertices = graph.get_vertices()
        optimal_pheromone_history: List[Any] = []

        # Определение стартовой вершины
        if self.first_vertex_index is not None:
            start_vertex = vertices[self.first_vertex_index]
        else:
            start_vertex = self.choose_start_vertex(vertices)

        self.initialize_pheromones(graph)

        for iteration in range(self.iterations):
            iteration_paths: List[List[Any]] = []
            # Если стартовая вершина не задана, выбираем случайно для каждой итерации.
            if self.first_vertex_index is None:
                start_vertex = self.choose_start_vertex(vertices)
            if self.show_plots:
                best_probability = self.calculate_best_paths_probability(
                    graph, best_paths
                )
                optimal_pheromone_history.append(
                    self.calculate_total_pheromone(best_paths, graph)
                )

            for ant in self.ants:
                current_vertex = start_vertex
                valid_path = True
                path = [start_vertex]

                for _ in range(len(vertices) - 1):
                    attractions = self.calculate_accessible_attraction(
                        ant, current_vertex, graph, path
                    )
                    if not attractions:
                        valid_path = False
                        break
                    next_vertex = self.choose_next_vertex(attractions)
                    if next_vertex is None:
                        valid_path = False
                        break
                    current_vertex = next_vertex
                    path.append(next_vertex)

                    # Если последний переход — возвращение к стартовой вершине
                    if len(path) == len(vertices):
                        delta = self.calculate_pheromone_change(
                            next_vertex, start_vertex, graph
                        )
                        if delta is not None:
                            path.append(start_vertex)
                        else:
                            valid_path = False
                        break

                if valid_path:
                    iteration_paths.append(path)
                    current_weight = graph.calculate_way_weight(path)
                    iter_weights.setdefault(iteration, []).append(current_weight)

                    if current_weight < min(path_weights):
                        best_paths = {tuple(path)}
                        best_paths_probability_history = []
                        optimal_pheromone_history = []
                    elif current_weight == min(path_weights):
                        best_paths.add(tuple(path))
                    path_weights.append(current_weight)

            if self.show_plots and best_probability is not None:
                best_paths_probability_history.append(best_probability)

            if self.evaporation_rate > 0:
                self.reduce_pheromones(graph)
            self.add_pheromones(iteration_paths, graph)

        if self.show_plots:
            best_paths_probability_history = self.fill_history(
                best_paths_probability_history
            )
            optimal_pheromone_history = self.fill_history(optimal_pheromone_history)
            avg_weight_history = self.get_avg_weight_per_10_iterations(iter_weights)

            iterations_axis = list(range(1, self.iterations + 1))
            iterations_avg_axis = list(range(10, len(avg_weight_history) + 10))

            fig, axs = plt.subplots(3, sharex=True)

            axs[0].plot(iterations_axis, best_paths_probability_history)
            axs[0].set_title("Вероятность оптимальных путей")
            axs[0].grid()

            axs[1].plot(iterations_avg_axis, avg_weight_history)
            axs[1].set_title("Средний вес пути (каждые 10 итераций)")
            axs[1].grid()

            axs[2].plot(iterations_axis, optimal_pheromone_history)
            axs[2].set_title("Суммарное количество феромона на оптимальных путях")
            axs[2].grid()

            if self.log_scale:
                axs[0].set_xscale("log")
                axs[1].set_xscale("log")
                axs[2].set_xscale("log")

            plt.show()

        best_weight = min(path_weights) if path_weights else None

        if best_paths:
            # Возвращаем минимальный вес и один из оптимальных путей.
            return best_weight, list(best_paths)[0]
        return None
