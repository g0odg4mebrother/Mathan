import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FunctionAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа: Нахождение характерных точек функции")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        self.x0_var = tk.StringVar(value="0")
        self.h_var = tk.StringVar(value="0.1")
        self.epsilon_var = tk.StringVar(value="0.001")
        self.max_iter_var = tk.StringVar(value="100")
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        input_frame = ttk.LabelFrame(main_frame, text="Входные данные", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        ttk.Label(input_frame, text="Начальное значение X0:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.x0_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Шаг h:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.h_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Точность (ε):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.epsilon_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Макс. итераций:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.max_iter_var, width=15).grid(row=3, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Найти точку пересечения", 
                  command=self.find_intersection).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Построить графики", 
                  command=self.plot_functions).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить результаты", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        result_frame = ttk.LabelFrame(main_frame, text="Результаты", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=10, wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        table_frame = ttk.LabelFrame(main_frame, text="Таблица итераций", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ('iteration', 'x', 'y1', 'y2', 'diff')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        self.tree.heading('iteration', text='Итерация')
        self.tree.heading('x', text='X')
        self.tree.heading('y1', text='Y1')
        self.tree.heading('y2', text='Y2')
        self.tree.heading('diff', text='|Y1-Y2|')
        
        self.tree.column('iteration', width=80, anchor='center')
        self.tree.column('x', width=100, anchor='center')
        self.tree.column('y1', width=120, anchor='center')
        self.tree.column('y2', width=120, anchor='center')
        self.tree.column('diff', width=120, anchor='center')
        
        tree_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=5)
        
    def calculate_y1(self, x):
        """Вычисление Y1 = (x^2 + 1) * sin(3 + x)"""
        return (x**2 + 1) * math.sin(3 + x)
    
    def calculate_y2(self, x):
        """Вычисление Y2 = (x + 5) / (x^2 + 1)"""
        return (x + 5) / (x**2 + 1)
    
    def find_intersection(self):
        """Поиск точки пересечения функций"""
        try:
            x0 = float(self.x0_var.get())
            h = float(self.h_var.get())
            epsilon = float(self.epsilon_var.get())
            max_iter = int(self.max_iter_var.get())
            
            self.clear_results()
            
            x = x0
            iteration = 0
            found = False
            
            self.result_text.insert(tk.END, "ПОИСК ТОЧКИ ПЕРЕСЕЧЕНИЯ\n")
            self.result_text.insert(tk.END, "="*60 + "\n")
            self.result_text.insert(tk.END, f"X0 = {x0}, h = {h}, ε = {epsilon}\n")
            self.result_text.insert(tk.END, "-"*60 + "\n")
            
            while iteration < max_iter:
                y1 = self.calculate_y1(x)
                y2 = self.calculate_y2(x)
                diff = abs(y1 - y2)
                
                self.tree.insert('', 'end', values=(
                    f"{iteration}",
                    f"{x:.4f}",
                    f"{y1:.6f}",
                    f"{y2:.6f}",
                    f"{diff:.6f}"
                ))
                
                self.result_text.insert(tk.END, f"Итер {iteration}: X={x:.4f}, Y1={y1:.6f}, Y2={y2:.6f}, |Y1-Y2|={diff:.6f}\n")
                
                if diff < epsilon:
                    found = True
                    result_message = (
                        f"\n{'='*50}\n"
                        f"ТОЧКА ПЕРЕСЕЧЕНИЯ НАЙДЕНА!\n"
                        f"X = {x:.6f}\n"
                        f"Y1 = Y2 = {y1:.6f}\n"
                        f"Погрешность: {diff:.6f}\n"
                        f"Количество итераций: {iteration}\n"
                        f"{'='*50}"
                    )
                    self.result_text.insert(tk.END, result_message)
                    self.status_var.set(f"Точка пересечения найдена: X={x:.4f}, Y={y1:.4f}")
                    
                    messagebox.showinfo("Успех", f"Точка пересечения найдена!\nX = {x:.4f}\nY = {y1:.4f}")
                    break
                
                x += h
                iteration += 1
            
            if not found:
                self.result_text.insert(tk.END, f"\nТочка пересечения не найдена за {max_iter} итераций")
                self.status_var.set(f"Точка пересечения не найдена за {max_iter} итераций")
                messagebox.showwarning("Предупреждение", f"Точка пересечения не найдена за {max_iter} итераций")
            
            self.result_text.see("1.0")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", "Введены некорректные данные!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
    
    def plot_functions(self):
        """Построение графиков функций"""
        try:
            x0 = float(self.x0_var.get())
            h = float(self.h_var.get())
            
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Графики функций")
            plot_window.geometry("800x600")
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
            
            x_start = min(-5, x0 - 2)
            x_end = max(5, x0 + 10)
            x_values = np.linspace(x_start, x_end, 500)
            
            y1_values = [(x**2 + 1) * math.sin(3 + x) for x in x_values]
            y2_values = [(x + 5) / (x**2 + 1) for x in x_values]
            
            ax1.plot(x_values, y1_values, 'b-', label='Y1 = (x²+1)·sin(3+x)', linewidth=2)
            ax1.plot(x_values, y2_values, 'r-', label='Y2 = (x+5)/(x²+1)', linewidth=2)
            ax1.set_xlabel('X')
            ax1.set_ylabel('Y')
            ax1.set_title('Графики функций Y1 и Y2')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            diff_values = [abs(y1 - y2) for y1, y2 in zip(y1_values, y2_values)]
            ax2.plot(x_values, diff_values, 'g-', label='|Y1 - Y2|', linewidth=2)
            ax2.axhline(y=0.001, color='r', linestyle='--', label='Порог ε=0.001')
            ax2.set_xlabel('X')
            ax2.set_ylabel('|Y1 - Y2|')
            ax2.set_title('Модуль разности функций')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_yscale('log')  
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            ttk.Button(plot_window, text="Закрыть", 
                      command=plot_window.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить графики: {e}")
    
    def clear_results(self):
        """Очистка результатов"""
        self.result_text.delete(1.0, tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.status_var.set("Результаты очищены")

def run_tests():
    """Запуск тестирования программы"""
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ПРОГРАММЫ (МЕТОДЫ БЕЛОГО ЯЩИКА)")
    print("="*60)
    
    test_cases = [
        {"name": "Тест 1 (покрытие операторов)", "x0": 0, "h": 0.1, "epsilon": 0.001, "max_iter": 20},
        {"name": "Тест 2 (покрытие решений)", "x0": 1, "h": 0.05, "epsilon": 0.001, "max_iter": 20},
        {"name": "Тест 3 (покрытие условий)", "x0": -1, "h": 0.1, "epsilon": 0.001, "max_iter": 20},
        {"name": "Тест 4 (комбинаторное)", "x0": 2, "h": 0.01, "epsilon": 0.001, "max_iter": 50}
    ]
    
    for test in test_cases:
        print(f"\n{test['name']}: X0={test['x0']}, h={test['h']}")
        print("-" * 40)
        
        x = test['x0']
        iteration = 0
        found = False
        
        print(f"{'Итер':^5} | {'X':^8} | {'Y1':^10} | {'Y2':^10} | {'|Y1-Y2|':^10}")
        print("-" * 55)
        
        while iteration < test['max_iter']:
            y1 = (x**2 + 1) * math.sin(3 + x)
            y2 = (x + 5) / (x**2 + 1)
            diff = abs(y1 - y2)
            
            print(f"{iteration:^5} | {x:^8.4f} | {y1:^10.6f} | {y2:^10.6f} | {diff:^10.6f}")
            
            if diff < test['epsilon']:
                print(f"\n>>> Точка пересечения найдена! X={x:.4f}, Y={y1:.4f}")
                found = True
                break
            
            x += test['h']
            iteration += 1
        
        if not found:
            print(f"\n>>> Точка пересечения не найдена за {test['max_iter']} итераций")

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionAnalyzer(root)
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Файл", menu=file_menu)
    file_menu.add_command(label="Очистить", command=app.clear_results)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)
    
    test_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Тестирование", menu=test_menu)
    test_menu.add_command(label="Запустить тесты (консоль)", command=run_tests)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Справка", menu=help_menu)
    help_menu.add_command(label="О программе", command=lambda: messagebox.showinfo(
        "О программе", 
        "Лабораторная работа\n"
        "Нахождение характерных точек функции\n\n"
        "Функции:\n"
        "Y1 = (x² + 1) · sin(3 + x)\n"
        "Y2 = (x + 5) / (x² + 1)"
    ))
    
    root.mainloop()