
import numpy as np

def solve_transport_problem(supply, demand, costs):

    print("Исходные данные:")
    print(f"Предложение поставщиков: A = {supply}")
    print(f"Спрос потребителей: B = {demand}")
    print("Матрица стоимостей:")
    print(np.array(costs))
    print()
    
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    print(f"Суммарное предложение: {total_supply}")
    print(f"Суммарный спрос: {total_demand}")
    
    if total_supply != total_demand:
        print("Задача несбалансированная!")
        return None
    
    m = len(supply)
    n = len(demand)
    
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    costs_copy = [row.copy() for row in costs]
    
    plan = [[0] * n for _ in range(m)]
    i, j = 0, 0
    
    print("Построение начального плана методом северо-западного угла:")
    
    while i < m and j < n:
        quantity = min(supply_copy[i], demand_copy[j])
        plan[i][j] = quantity
        
        print(f"  x{i+1}{j+1} = {quantity}")

        supply_copy[i] -= quantity
        demand_copy[j] -= quantity

        if supply_copy[i] == 0 and i < m - 1:
            i += 1
        elif demand_copy[j] == 0 and j < n - 1:
            j += 1
        else:
            if i < m - 1:
                i += 1
            if j < n - 1:
                j += 1
    
    print("\nНачальный план перевозок:")
    print_plan(plan, costs)
    
    initial_cost = calculate_total_cost(plan, costs)
    print(f"Начальная стоимость: {initial_cost}")
    
    print("\n" + "="*50)
    print("Оптимизация методом потенциалов")
    print("="*50)
    
    iteration = 1
    while True:
        print(f"\nИтерация {iteration}:")
        
        u = [None] * m
        v = [None] * n
        u[0] = 0  
        
        changed = True
        while changed:
            changed = False
            for i in range(m):
                for j in range(n):
                    if plan[i][j] > 0:  
                        if u[i] is not None and v[j] is None:
                            v[j] = costs[i][j] - u[i]
                            changed = True
                        elif u[i] is None and v[j] is not None:
                            u[i] = costs[i][j] - v[j]
                            changed = True
        
        print("Потенциалы:")
        print(f"u = {u}")
        print(f"v = {v}")
        
        optimal = True
        max_delta = 0
        max_i, max_j = -1, -1
        
        for i in range(m):
            for j in range(n):
                if plan[i][j] == 0:  
                    delta = costs[i][j] - (u[i] + v[j])
                    if delta < 0:
                        optimal = False
                        if delta < max_delta:
                            max_delta = delta
                            max_i, max_j = i, j
        
        if optimal:
            print("План оптимален!")
            break
        
        print(f"Клетка для улучшения: ({max_i+1}, {max_j+1}) с оценкой {max_delta}")
        
        cycle = find_cycle(plan, max_i, max_j)
        print("Цикл пересчета:", cycle)
        
        min_quantity = float('inf')
        for k in range(1, len(cycle), 2): 
            i, j = cycle[k]
            if plan[i][j] < min_quantity:
                min_quantity = plan[i][j]
        
        print(f"Минимальное значение в четных вершинах: {min_quantity}")

        for k, (i, j) in enumerate(cycle):
            if k % 2 == 0: 
                plan[i][j] += min_quantity
            else:  
                plan[i][j] -= min_quantity
        
        for i in range(m):
            for j in range(n):
                if plan[i][j] < 0.0001: 
                    plan[i][j] = 0
        
        print("Новый план:")
        print_plan(plan, costs)
        
        current_cost = calculate_total_cost(plan, costs)
        print(f"Текущая стоимость: {current_cost}")
        
        iteration += 1
    
    return plan, current_cost

def find_cycle(plan, start_i, start_j):
    """
    Нахождение цикла пересчета для заданной клетки
    """
    m = len(plan)
    n = len(plan[0])
    
    basis = []
    for i in range(m):
        for j in range(n):
            if plan[i][j] > 0:
                basis.append((i, j))
    
    basis.append((start_i, start_j))
    
    rows = {}
    cols = {}
    
    for i, j in basis:
        if i not in rows:
            rows[i] = []
        rows[i].append((i, j))
        
        if j not in cols:
            cols[j] = []
        cols[j].append((i, j))
    
    def dfs(current, target, visited, path, direction):
        if current == target and len(path) > 2:
            return path.copy()
        
        i, j = current
        
        if direction == 'row':
            for next_cell in rows[i]:
                if next_cell not in visited:
                    visited.add(next_cell)
                    path.append(next_cell)
                    result = dfs(next_cell, target, visited, path, 'col')
                    if result:
                        return result
                    path.pop()
                    visited.remove(next_cell)
        else:
            for next_cell in cols[j]:
                if next_cell not in visited:
                    visited.add(next_cell)
                    path.append(next_cell)
                    result = dfs(next_cell, target, visited, path, 'row')
                    if result:
                        return result
                    path.pop()
                    visited.remove(next_cell)
        
        return None
    
    start = (start_i, start_j)
    visited = {start}
    path = [start]
    
    cycle = dfs(start, start, visited, path, 'row')
    
    if cycle:
        return cycle
    else:
        visited = {start}
        path = [start]
        cycle = dfs(start, start, visited, path, 'col')
        return cycle

def calculate_total_cost(plan, costs):
    """Расчет общей стоимости перевозок"""
    total = 0
    for i in range(len(plan)):
        for j in range(len(plan[0])):
            total += plan[i][j] * costs[i][j]
    return total

def print_plan(plan, costs):
    """Вывод плана перевозок"""
    m = len(plan)
    n = len(plan[0])
    
    print("   ", end="")
    for j in range(n):
        print(f"B{j+1:3} ", end="")
    print()
    
    for i in range(m):
        print(f"A{i+1} ", end="")
        for j in range(n):
            if plan[i][j] > 0:
                print(f"{plan[i][j]:3}* ", end="")
            else:
                print(f"{plan[i][j]:3}  ", end="")
        print()
    
    print("Стоимости перевозок в базисных клетках:")
    for i in range(m):
        for j in range(n):
            if plan[i][j] > 0:
                print(f"  x{i+1}{j+1}: {plan[i][j]} * {costs[i][j]} = {plan[i][j] * costs[i][j]}")

def main():

    supply = [90, 40, 70]  # a1, a2, a3
    demand = [50, 50, 100]  # b1, b2, b3
    costs = [
        [3, 4, 2],
        [5, 6, 1],
        [8, 3, 5]
    ]
    
    print("ТРАНСПОРТНАЯ ЗАДАЧА (Вариант 1)")
    print("="*50)
    
    optimal_plan, min_cost = solve_transport_problem(supply, demand, costs)
    
    if optimal_plan:
        print("\n" + "="*50)
        print("ОПТИМАЛЬНЫЙ ПЛАН ПЕРЕВОЗОК:")
        print("="*50)
        print_plan(optimal_plan, costs)
        print(f"\nМИНИМАЛЬНАЯ СТОИМОСТЬ: {min_cost}")
        
        print("\nРАСШИФРОВКА ПЛАНА:")
        total = 0
        for i in range(len(optimal_plan)):
            for j in range(len(optimal_plan[0])):
                if optimal_plan[i][j] > 0:
                    print(f"  От поставщика A{i+1} к потребителю B{j+1}: {optimal_plan[i][j]} ед. по цене {costs[i][j]} = {optimal_plan[i][j] * costs[i][j]}")
                    total += optimal_plan[i][j] * costs[i][j]
        print(f"  ИТОГО: {total}")

if __name__ == "__main__":
    main()