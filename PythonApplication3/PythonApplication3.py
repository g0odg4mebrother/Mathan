import numpy as np
import itertools
import tkinter as tk


def find_vertices(lines, check):
    points = []
    for (A1, b1), (A2, b2) in itertools.combinations(lines, 2):
        A = np.array([A1, A2])
        b = np.array([b1, b2])

        if np.linalg.det(A) != 0:
            x = np.linalg.solve(A, b)
            if check(x[0], x[1]):
                points.append((x[0], x[1]))
    return points


scale = 60
offset = 50

def to_canvas(x, y):
    return offset + x*scale, 450 - y*scale

def draw_axes():
    canvas.create_line(50, 450, 550, 450)
    canvas.create_line(50, 450, 50, 50)

def draw_points(points):
    for x, y in points:
        cx, cy = to_canvas(x, y)
        canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill="red")


def system_a():
    canvas.delete("all")
    draw_axes()

    lines = [
        ([1, 3], 3),
        ([-2, 1], 2),
        ([1, 1], 5),
        ([1, 0], 0),
        ([0, 1], 0)
    ]

    def check(x1, x2):
        return (x1 + 3*x2 >= 3 and
                -2*x1 + x2 <= 2 and
                x1 + x2 <= 5 and
                x1 >= 0 and x2 >= 0)

    points = find_vertices(lines, check)
    draw_points(points)

    result_label.config(text=f"Вершины (a):\n{points}")


def system_b():
    canvas.delete("all")
    draw_axes()

    lines = [
        ([1, -1], 3),
        ([2, 1], 3),
        ([1, -3], 1),
        ([1, 0], 0),
        ([0, 1], 0)
    ]

    def check(x1, x2):
        return (x1 - x2 <= 3 and
                2*x1 + x2 >= 3 and
                x1 - 3*x2 <= 1 and
                x1 >= 0 and x2 >= 0)

    points = find_vertices(lines, check)
    draw_points(points)

    result_label.config(text=f"Вершины (b):\n{points}")

def production_task():
    canvas.delete("all")
    draw_axes()

    lines = [
        ([0.2, 0.1], 100),
        ([0.2, 0.5], 180),
        ([0.1, 0.2], 100),
        ([1, 0], 300),
        ([0, 1], 200),
        ([1, 0], 0),
        ([0, 1], 0)
    ]

    def check(x1, x2):
        return (0.2*x1 + 0.1*x2 <= 100 and
                0.2*x1 + 0.5*x2 <= 180 and
                0.1*x1 + 0.2*x2 <= 100 and
                x1 >= 300 and
                x2 <= 200 and
                x1 >= 0 and x2 >= 0)

    points = find_vertices(lines, check)

    max_profit = 0
    best_point = None

    for x1, x2 in points:
        profit = 100*x1 + 160*x2
        if profit > max_profit:
            max_profit = profit
            best_point = (x1, x2)

    draw_points(points)

    if best_point:
        result_label.config(
            text=f"Оптимальный план:\n"
                 f"x1 = {round(best_point[0],2)}\n"
                 f"x2 = {round(best_point[1],2)}\n"
                 f"Прибыль = {round(max_profit,2)}"
        )
    else:
        result_label.config(text="Допустимых решений нет")

window = tk.Tk()
window.title("Решение задач ЛП")

canvas = tk.Canvas(window, width=600, height=500, bg="white")
canvas.pack()

frame = tk.Frame(window)
frame.pack()

tk.Button(frame, text="Система (a)", command=system_a).pack(side="left", padx=10)
tk.Button(frame, text="Система (b)", command=system_b).pack(side="left", padx=10)
tk.Button(frame, text="Производственная задача", command=production_task).pack(side="left", padx=10)

result_label = tk.Label(window, text="", font=("Arial", 11))
result_label.pack(pady=10)


window.mainloop()
