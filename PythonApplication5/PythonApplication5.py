import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

a = 1.0
L = 10.0
T = 1.0
h = 0.1
tau = 0.004

sigma = a * tau / h**2
if sigma > 0.5:
    raise ValueError("Нарушено условие устойчивости: sigma должно быть <= 0.5")

x = np.arange(-L, L + h, h)
t = np.arange(0, T + tau, tau)

Nx = len(x)
Nt = len(t)

U = np.zeros((Nt, Nx))
U[0, :] = np.exp(-x**2)

for j in range(0, Nt - 1):
    for i in range(1, Nx - 1):
        U[j+1, i] = (
            U[j, i] +
            sigma * (U[j, i-1] - 2*U[j, i] + U[j, i+1])
        )
    U[j+1, 0] = 0
    U[j+1, -1] = 0


root = tk.Tk()
root.title("Задача Коши — уравнение теплопроводности")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

fig = Figure(figsize=(7, 5))
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def plot_solution(time_index):
    ax.clear()
    ax.plot(x, U[time_index, :])
    ax.set_xlabel("x")
    ax.set_ylabel("u(x,t)")
    ax.set_title(f"t = {round(t[time_index], 3)}")
    ax.grid(True)
    canvas.draw()

slider = tk.Scale(
    root,
    from_=0,
    to=Nt-1,
    orient=tk.HORIZONTAL,
    length=600,
    label="Выберите момент времени",
    command=lambda val: plot_solution(int(val))
)
slider.pack()

plot_solution(0)

root.mainloop()