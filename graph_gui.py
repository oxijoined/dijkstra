# Файл graph_gui.py

import tkinter as tk
from math import pi, cos, sin
import pickle
from tkinter import simpledialog
from tkinter import ttk
import tkinter.filedialog
from tkinter import messagebox
from graph import Graph
import random


class GraphGui:
    def __init__(self):
        self.graph = Graph()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()
        self.vertices_coordinates = {}  # добавляем эту строку

        # Определяем меню
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Загрузить граф", command=self.load_graph)
        filemenu.add_command(label="Сохранить граф", command=self.save_graph)
        filemenu.add_command(label="Добавить вершину", command=self.add_vertex)
        filemenu.add_command(label="Добавить ребро", command=self.add_edge)

        algorithmmenu = tk.Menu(menu)
        menu.add_cascade(label="Алгоритм", menu=algorithmmenu)
        algorithmmenu.add_command(label="Алгоритм Дейкстры", command=self.run_dijkstra)

        # Определяем привязку событий
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

    def on_canvas_right_click(self, event):
        # Создаем новое ребро при перетаскивании мыши с зажатой кнопкой
        start_vertex = self.get_vertex_at(event.x, event.y)
        if start_vertex is not None:
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавление вершины")

            # Создаем поля ввода для конечной вершины и веса
            tk.Label(dialog, text="Конечная вершина:").grid(row=0)
            end = tk.Entry(dialog)
            end.grid(row=0, column=1)

            tk.Label(dialog, text="Вес ребра:").grid(row=1)
            weight = tk.Entry(dialog)
            weight.grid(row=1, column=1)

            # Добавляем кнопку, которая добавляет ребро в граф и заново рисует его
            tk.Button(
                dialog,
                text="Add edge",
                command=lambda: self._add_edge_callback(
                    start_vertex, end, weight, dialog
                ),
            ).grid(row=2, column=0, columnspan=2)

    def _add_edge_callback(self, start_vertex, end_entry, weight_entry, dialog):
        end_vertex = end_entry.get()
        weight = weight_entry.get()

        if end_vertex and weight:
            if end_vertex in self.graph.get_vertices():
                self.graph.add_edge(start_vertex, end_vertex, int(weight))
                self.draw_graph()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Конечная вершина не существует.")
        else:
            messagebox.showerror("Ошибка", "Оба поля должны быть заполнены.")

    def on_canvas_click(self, event):
        # Запрашиваем имя вершины у пользователя
        name = simpledialog.askstring("Input", "Enter vertex name:")
        if name is not None:
            self.graph.add_vertex(name)
            self.vertices_coordinates[name] = (event.x, event.y)
            self.draw_graph()

    def save_graph(self):
        file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".pickle")
        if file_name is not None:
            with open(file_name, "wb") as f:
                pickle.dump(self.graph, f)
            messagebox.showinfo("Сохранить", "Граф успешно сохранен.")

    def load_graph(self):
        file_name = tkinter.filedialog.askopenfilename(
            filetypes=[("Pickle files", "*.pickle")]
        )
        if file_name is not None:
            with open(file_name, "rb") as f:
                self.graph = pickle.load(f)
            self.draw_graph()
            messagebox.showinfo("Загрузка", "Граф успешно загружен.")

    def get_vertex_at(self, x, y):
        # Возвращает вершину, расположенную в координатах (x, y), или None
        for vertex, (vx, vy) in self.vertices_coordinates.items():
            if abs(vx - x) < 20 and abs(vy - y) < 20:
                return vertex
        return None

    def add_vertex(self):
        # Добавление вершины через меню
        name = simpledialog.askstring("Ввод", "Введите имя вершины:")
        if name is not None:
            self.graph.add_vertex(name)
            self.draw_graph()

    def add_edge(self):
        # Создаем новое окно
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить вершину")

        # Создаем поля ввода и выпадающие списки для выбора вершин
        tk.Label(dialog, text="Начальная вершина:").grid(row=0)
        start = ttk.Combobox(dialog, values=list(self.graph.get_vertices()))
        start.grid(row=0, column=1)

        tk.Label(dialog, text="Конечная вершина:").grid(row=1)
        end = ttk.Combobox(dialog, values=list(self.graph.get_vertices()))
        end.grid(row=1, column=1)

        tk.Label(dialog, text="Вес ребра:").grid(row=2)
        weight = tk.Entry(dialog)
        weight.grid(row=2, column=1)

        # Добавляем кнопку, которая добавляет ребро в граф и заново рисует его
        tk.Button(
            dialog,
            text="Add edge",
            command=lambda: self._add_edge_callback(start, end, weight),
        ).grid(row=3, column=0, columnspan=2)

    def run_dijkstra(self):
        start = simpledialog.askstring("Вход", "Введите начальную вершину:")
        if start is not None:
            self.draw_dijkstra(start)

    def draw_graph(self):
        # Очищаем холст
        self.canvas.delete("all")

        # Задаем координаты для вершин
        vertices = list(self.graph.get_vertices())
        n = len(vertices)  # количество вершин
        center_x, center_y = 400, 300  # центр холста
        radius = 200  # радиус круга

        self.vertices_coordinates = {}
        for i, vertex in enumerate(vertices):
            angle = 2 * pi * i / n  # угол в радианах
            x = center_x + radius * cos(angle)
            y = center_y + radius * sin(angle)
            self.vertices_coordinates[vertex] = (x, y)

        # Рисуем ребра
        for start, end, weight in self.graph.get_edges():
            start_x, start_y = self.vertices_coordinates[start]
            end_x, end_y = self.vertices_coordinates[end]
            self.canvas.create_line(start_x, start_y, end_x, end_y)
            self.canvas.create_text(
                (start_x + end_x) / 2, (start_y + end_y) / 2, text=str(weight)
            )

        # Рисуем вершины
        for vertex, (x, y) in self.vertices_coordinates.items():
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
            self.canvas.create_text(x, y, text=vertex)

    def draw_dijkstra(self, start):
        # Выполняем алгоритм Дейкстры
        distances, paths = self.graph.dijkstra(start)

        # Очищаем холст и заново рисуем граф
        self.draw_graph()

        # Рисуем метки Дейкстры
        for vertex, distance in distances.items():
            x, y = self.vertices_coordinates[vertex]
            self.canvas.create_text(x, y - 30, text=str(distance))

        # Рисуем пути Дейкстры
        for vertex, path in paths.items():
            for i in range(len(path) - 1):
                start, end = path[i], path[i + 1]
                start_x, start_y = self.vertices_coordinates[start]
                end_x, end_y = self.vertices_coordinates[end]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red")

    def run(self):
        self.root.mainloop()
