# Файл graph.py
import sys
import heapq
from typing import Dict, List, Optional, Tuple


class Graph:
    def __init__(self):
        # Словарь, где ключ - имя вершины, а значение - словарь с соседями и весами ребер
        self.vertices: Dict[str, Dict[str, int]] = {}

    def add_vertex(self, name: str) -> None:
        """
        Добавляет новую вершину в граф.

        :param name: имя новой вершины.
        """
        if name not in self.vertices:
            self.vertices[name] = {}

    def add_edge(self, start: str, end: str, weight: int) -> None:
        """
        Добавляет новое ребро в граф.

        :param start: имя начальной вершины ребра.
        :param end: имя конечной вершины ребра.
        :param weight: вес ребра.
        """
        if start not in self.vertices or end not in self.vertices:
            raise ValueError("One or both vertices are not found in the graph")

        # Добавляем связь в обе стороны, так как граф ненаправленный
        self.vertices[start][end] = weight
        self.vertices[end][start] = weight

    def get_vertices(self) -> List[str]:
        """
        Возвращает список всех вершин графа.

        :return: список имен вершин.
        """
        return list(self.vertices.keys())

    def get_edges(self) -> List[Tuple[str, str, int]]:
        """
        Возвращает список всех ребер графа.

        :return: список кортежей, где каждый кортеж представляет ребро и состоит из имени начальной вершины,
                 имени конечной вершины и веса ребра.
        """
        edges = []
        for vertex, neighbours in self.vertices.items():
            for neighbour, weight in neighbours.items():
                # Добавляем ребро только в одну сторону, чтобы избежать дубликатов
                if (neighbour, vertex, weight) not in edges:
                    edges.append((vertex, neighbour, weight))
        return edges

    def dijkstra(self, start: str) -> Dict[str, Tuple[int, List[str]]]:
        """
        Реализует алгоритм Дейкстры для поиска кратчайшего пути от одной вершины до всех остальных.

        :param start: имя начальной вершины.
        :return: словарь, где ключ - имя конечной вершины, а значение - кортеж, состоящий из длины кратчайшего пути
                 и списка вершин в этом пути.
        """
        # Инициализация
        distances = {vertex: float("infinity") for vertex in self.vertices}
        distances[start] = 0
        paths = {vertex: [] for vertex in self.vertices}
        paths[start] = [start]

        # Очередь приоритетов с вершинами
        queue = [(0, start)]

        while queue:
            # Извлекаем вершину с минимальным расстоянием
            current_distance, current_vertex = heapq.heappop(queue)

            # Проверяем все соседние вершины
            for neighbor in self.vertices[current_vertex]:
                weight = self.vertices[current_vertex][neighbor]
                distance = current_distance + weight

                # Обновляем расстояние и путь, если найден более короткий
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    paths[neighbor] = paths[current_vertex] + [neighbor]
                    heapq.heappush(queue, (distance, neighbor))

        return distances, paths
