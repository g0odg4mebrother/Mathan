import numpy as np
import itertools

def solve_system_1a():
    print("=" * 60)
    print("Задача 1а: Решение системы неравенств")
    print("=" * 60)
    print("Система неравенств:")
    print("1) x₁ + 3x₂ ≥ 3")
    print("2) -2x₁ + x₂ ≤ 2")
    print("3) x₁ + x₂ ≤ 5")
    print("4) x₁ ≥ 0, x₂ ≥ 0")
    print()

    
    def solve_l1_l2():

        A = np.array([[1, 3], [-2, 1]])
        b = np.array([3, 2])
        try:
            return np.linalg.solve(A, b)
        except:
            return None
    
    def solve_l1_l3():

        A = np.array([[1, 3], [1, 1]])
        b = np.array([3, 5])
        try:
            return np.linalg.solve(A, b)
        except:
            return None
    
    def solve_l1_l4():

        return np.array([0, 1])
    
    def solve_l1_l5():

        return np.array([3, 0])
    
    def solve_l2_l3():

        A = np.array([[-2, 1], [1, 1]])
        b = np.array([2, 5])
        try:
            return np.linalg.solve(A, b)
        except:
            return None
    
    def solve_l2_l4():

        return np.array([0, 2])
    
    def solve_l2_l5():

        return np.array([-1, 0])
    
    def solve_l3_l4():

        return np.array([0, 5])
    
    def solve_l3_l5():

        return np.array([5, 0])
    
    intersection_points = []
    
    points = [
        solve_l1_l2(), solve_l1_l3(), solve_l1_l4(), solve_l1_l5(),
        solve_l2_l3(), solve_l2_l4(), solve_l2_l5(),
        solve_l3_l4(), solve_l3_l5()
    ]
    
    for point in points:
        if point is not None:
            is_unique = True
            for existing in intersection_points:
                if np.allclose(point, existing, rtol=1e-10, atol=1e-10):
                    is_unique = False
                    break
            if is_unique:
                intersection_points.append(point)
    
    print("Все точки пересечения линий:")
    for i, point in enumerate(intersection_points):
        print(f"  Точка {i+1}: ({point[0]:.4f}, {point[1]:.4f})")
    
    feasible_points = []
    for point in intersection_points:
        x1, x2 = point
        
        # Проверяем все неравенства
        ineq1 = x1 + 3*x2 >= 3 - 1e-10
        ineq2 = -2*x1 + x2 <= 2 + 1e-10
        ineq3 = x1 + x2 <= 5 + 1e-10
        ineq4 = x1 >= -1e-10
        ineq5 = x2 >= -1e-10
        
        if ineq1 and ineq2 and ineq3 and ineq4 and ineq5:
            feasible_points.append(point)
    
    print("\nУгловые точки области допустимых решений (ОДР):")
    for i, point in enumerate(feasible_points):
        print(f"  Точка {i+1}: ({point[0]:.4f}, {point[1]:.4f})")
    
    print("\nДля графического представления можно построить линии:")
    print("  L1: x₂ = (3 - x₁)/3")
    print("  L2: x₂ = 2x₁ + 2")
    print("  L3: x₂ = 5 - x₁")
    print()
    
    x1_values = np.linspace(0, 6, 10)
    print("Таблица значений для построения линий:")
    print("x₁\tL1(x₂)\tL2(x₂)\tL3(x₂)")
    print("-" * 40)
    for x1 in x1_values:
        l1 = (3 - x1) / 3
        l2 = 2*x1 + 2
        l3 = 5 - x1
        print(f"{x1:.2f}\t{l1:.2f}\t{l2:.2f}\t{l3:.2f}")
    
    print("\n" + "=" * 60)

def solve_system_1b():
    print("=" * 60)
    print("Задача 1б: Решение системы неравенств")
    print("=" * 60)
    print("Система неравенств:")
    print("1) -x₁ + 3x₂ ≤ 9")
    print("2) 2x₁ + 3x₂ ≤ 18")
    print("3) 2x₁ - x₂ ≤ 10")
    print("4) x₁ ≥ 0, x₂ ≥ 0")
    print()
    
    def solve_l1_l2():

        A = np.array([[-1, 3], [2, 3]])
        b = np.array([9, 18])
        try:
            return np.linalg.solve(A, b)
        except:
            return None
    
    def solve_l1_l3():

        A = np.array([[-1, 3], [2, -1]])
        b = np.array([9, 10])
        try:
            return np.linalg.solve(A, b)
        except:
            return None
    
    def solve_l1_l4():

        return np.array([0, 3])
    
    def solve_l1_l5():

        return np.array([-9, 0])
    
    def solve_l2_l3():

        A = np.array([[2, 3], [2, -1]])
        b = np.array([18, 10])
        try:
            return np.linalg.solve(A, b)
        except:
            return None
    
    def solve_l2_l4():

        return np.array([0, 6])
    
    def solve_l2_l5():

        return np.array([9, 0])
    
    def solve_l3_l4():

        return np.array([0, -10])
    
    def solve_l3_l5():

        return np.array([5, 0])
    
    intersection_points = []
    
    points = [
        solve_l1_l2(), solve_l1_l3(), solve_l1_l4(), solve_l1_l5(),
        solve_l2_l3(), solve_l2_l4(), solve_l2_l5(),
        solve_l3_l4(), solve_l3_l5()
    ]
    
    for point in points:
        if point is not None:
            is_unique = True
            for existing in intersection_points:
                if np.allclose(point, existing, rtol=1e-10, atol=1e-10):
                    is_unique = False
                    break
            if is_unique:
                intersection_points.append(point)
    
    print("Все точки пересечения линий:")
    for i, point in enumerate(intersection_points):
        print(f"  Точка {i+1}: ({point[0]:.4f}, {point[1]:.4f})")
    
    feasible_points = []
    for point in intersection_points:
        x1, x2 = point
        
        ineq1 = -x1 + 3*x2 <= 9 + 1e-10
        ineq2 = 2*x1 + 3*x2 <= 18 + 1e-10
        ineq3 = 2*x1 - x2 <= 10 + 1e-10
        ineq4 = x1 >= -1e-10
        ineq5 = x2 >= -1e-10
        
        if ineq1 and ineq2 and ineq3 and ineq4 and ineq5:
            feasible_points.append(point)
    
    print("\nУгловые точки области допустимых решений (ОДР):")
    for i, point in enumerate(feasible_points):
        print(f"  Точка {i+1}: ({point[0]:.4f}, {point[1]:.4f})")
    
    print("\nДля графического представления можно построить линии:")
    print("  L1: x₂ = (9 + x₁)/3")
    print("  L2: x₂ = (18 - 2x₁)/3")
    print("  L3: x₂ = 2x₁ - 10")
    print()
    
    x1_values = np.linspace(0, 10, 11)
    print("Таблица значений для построения линий:")
    print("x₁\tL1(x₂)\tL2(x₂)\tL3(x₂)")
    print("-" * 45)
    for x1 in x1_values:
        l1 = (9 + x1) / 3
        l2 = (18 - 2*x1) / 3
        l3 = 2*x1 - 10
        l3_display = l3 if l3 >= 0 else "отр."
        print(f"{x1:.2f}\t{l1:.2f}\t{l2:.2f}\t{l3_display}")
    
    print("\n" + "=" * 60)

def solve_production_optimization():
    print("=" * 60)
    print("Задача 2: Оптимизация производства")
    print("=" * 60)

    c = np.array([30, 25, 56, 48])
    
    A = np.array([
        [3, 5, 2, 4],   
        [22, 14, 18, 30], 
        [10, 14, 8, 16]   
    ])
    
    b = np.array([60, 400, 130])
    
    print("Исходные данные:")
    print("Прибыль на единицу товара:")
    for i, profit in enumerate(c, 1):
        print(f"  Товар {i}: {profit} руб.")
    
    print("\nЗатраты ресурсов на единицу товара:")
    print("Ресурс\t\tТ1\tТ2\tТ3\tТ4\tВсего")
    print("-" * 55)
    resources = ["Сырье (кг)", "Раб.сила (чел)", "Оборуд.(ст.ч)"]
    for i, (res_name, row) in enumerate(zip(resources, A)):
        print(f"{res_name}\t{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{b[i]}")
    
    print("\n" + "=" * 60)
    print("Поиск оптимального решения перебором угловых точек")
    print("=" * 60)
    
    n_vars = 4
    n_constraints = 3
    
    best_solution = None
    best_profit = -np.inf
    
    for basis in itertools.combinations(range(n_vars + n_constraints), n_constraints):

        A_slack = np.hstack([A, np.eye(n_constraints)])
        c_slack = np.hstack([c, np.zeros(n_constraints)])
        
        try:
            B = A_slack[:, list(basis)]
            if np.linalg.det(B) == 0:
                continue
            
            x_B = np.linalg.solve(B, b)
            
            if np.any(x_B < -1e-10):
                continue
            
            x_full = np.zeros(n_vars + n_constraints)
            x_full[list(basis)] = x_B
            
            x = x_full[:n_vars]
            
            if np.all(A @ x <= b + 1e-10) and np.all(x >= -1e-10):
                profit = c @ x
                
                if profit > best_profit:
                    best_profit = profit
                    best_solution = x.copy()
                    
        except np.linalg.LinAlgError:
            continue
    
    if best_solution is not None:
        print("\nОптимальный план производства:")
        for i, val in enumerate(best_solution, 1):
            if val > 1e-10: 
                print(f"  Товар {i}: {val:.4f} ед.")
            else:
                print(f"  Товар {i}: 0.0000 ед.")
        
        print(f"\nМаксимальная прибыль: {best_profit:.4f} руб.")
        
        print("\nИспользование ресурсов:")
        usage = A @ best_solution
        for i, (res_name, used, total) in enumerate(zip(resources, usage, b)):
            remainder = total - used
            print(f"  {res_name}: {used:.4f} / {total} (остаток: {remainder:.4f})")
        
        print("\nАнализ использования ресурсов:")
        for i, (res_name, used, total) in enumerate(zip(resources, usage, b)):
            if abs(used - total) < 1e-10:
                print(f"  {res_name}: дефицитный ресурс (использован полностью)")
            else:
                print(f"  {res_name}: недефицитный ресурс (остаток: {total - used:.4f})")
    else:
        print("Не удалось найти допустимое решение")

def main():
    solve_system_1a()
    
    # Решаем задачу 1б
    solve_system_1b()
    
    # Решаем задачу 2
    solve_production_optimization()

if __name__ == "__main__":
    main()