
import math

def zadacha_1():
    print("\n" + "="*60)
    print("ЗАДАЧА 1. Оптимальное распределение средств между предприятиями")
    print("="*60)
    
    S0 = 900 
    n = 4    

    def dohod_A(x):
        return 4 * x
    
    def dohod_B(y):
        return 5 * y
    
    def ostatok_A(x):
        return 0.3 * x
    
    def ostatok_B(y):
        return 0.1 * y

    dp = [[-float('inf')] * (S0 + 1) for _ in range(n + 1)]
    choice = [[0] * (S0 + 1) for _ in range(n + 1)]
    
    for s in range(S0 + 1):
        dp[0][s] = 0
    
    for k in range(1, n + 1):
        for s in range(S0 + 1):
            max_dohod = -float('inf')
            best_x = 0
            
            for x in range(s + 1):
                y = s - x
                
                current_dohod = dohod_A(x) + dohod_B(y)
                
                next_s = ostatok_A(x) + ostatok_B(y)
                next_s = int(round(next_s))  
                
                if next_s > S0:
                    next_s = S0
                
                total = current_dohod + dp[k-1][next_s]
                
                if total > max_dohod:
                    max_dohod = total
                    best_x = x
            
            dp[k][s] = max_dohod
            choice[k][s] = best_x
    
    print(f"\nРезультат распределения средств на {n} кварталов:")
    print(f"Начальная сумма: {S0} единиц")
    print(f"Максимальный возможный доход: {dp[n][S0]:.2f} единиц\n")
    
    print("Поквартальное распределение:")
    print("-" * 60)
    print(f"{'Квартал':<8} {'Средства в начале':<18} {'Предпр. А':<12} {'Предпр. Б':<12} {'Доход':<12}")
    print("-" * 60)
    
    s = S0
    total_dohod = 0
    
    for k in range(n, 0, -1):
        x = choice[k][s]
        y = s - x
        
        dohod_a = dohod_A(x)
        dohod_b = dohod_B(y)
        kvart_dohod = dohod_a + dohod_b
        total_dohod += kvart_dohod
        
        ostatok = ostatok_A(x) + ostatok_B(y)
        
        print(f"{n-k+1:<8} {s:<18.2f} {x:<12.2f} {y:<12.2f} {kvart_dohod:<12.2f}")
        
        s = int(round(ostatok))
    
    print("-" * 60)
    print(f"ИТОГО ДОХОД ЗА ГОД: {total_dohod:.2f} единиц")
    print()

def zadacha_2():
    print("\n" + "="*60)
    print("ЗАДАЧА 2. Поиск кратчайшего пути от точки 1 до точки 10")
    print("="*60)
    
    print("\nТак как точные данные графа на изображении не распознаны,")
    print("предлагаю ввести граф вручную.")
    print("\nВарианты ввода:")
    print("1. Ввести граф с клавиатуры")
    print("2. Использовать тестовый пример")
    
    choice = input("\nВыберите вариант (1 или 2): ").strip()
    
    graph = {}
    
    if choice == "1":
        print("\nВведите количество ребер:")
        m = int(input().strip())
        print("\nВводите ребра в формате: u v w (откуда куда вес)")
        print("Пример: 1 2 7")
        
        for i in range(m):
            u, v, w = map(int, input().split())
            if u not in graph:
                graph[u] = []
            graph[u].append((v, w))
    else:
        print("\nИспользуется тестовый граф:")
        edges = [
            (1, 2, 7), (1, 3, 9), (1, 6, 14),
            (2, 1, 7), (2, 3, 10), (2, 4, 15),
            (3, 1, 9), (3, 2, 10), (3, 4, 11), (3, 6, 2),
            (4, 2, 15), (4, 3, 11), (4, 5, 6),
            (5, 4, 6), (5, 10, 9),
            (6, 1, 14), (6, 3, 2), (6, 5, 9),
            (7, 6, 1), (7, 8, 2),
            (8, 7, 2), (8, 9, 3),
            (9, 8, 3), (9, 10, 4),
            (10, 5, 9), (10, 9, 4), (10, 7, 3)
        ]
        
        for u, v, w in edges:
            if u not in graph:
                graph[u] = []
            graph[u].append((v, w))
        
        print("Ребра:")
        for u, v, w in edges:
            print(f"  {u} -> {v} : {w}")
    
    start = 1
    target = 10
    
    vertices = set()
    for u in graph:
        vertices.add(u)
        for v, _ in graph[u]:
            vertices.add(v)
    
    dist = {v: float('inf') for v in vertices}
    prev = {v: None for v in vertices}
    dist[start] = 0
    visited = set()
    
    while len(visited) < len(vertices):
        current = None
        min_dist = float('inf')
        
        for v in vertices:
            if v not in visited and dist[v] < min_dist:
                min_dist = dist[v]
                current = v
        
        if current is None:
            break
        
        visited.add(current)
        
        if current in graph:
            for neighbor, weight in graph[current]:
                new_dist = dist[current] + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current
    
    print(f"\nРезультат поиска пути от {start} до {target}:")
    print("-" * 60)
    
    if dist[target] == float('inf'):
        print(f"Путь из вершины {start} в вершину {target} не существует!")
    else:
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()
        
        print(f"Кратчайшее расстояние: {dist[target]}")
        print(f"Кратчайший путь: {' -> '.join(map(str, path))}")
    
    print()

def main():
    print("\n" + "="*60)
    print("РЕШЕНИЕ ЗАДАЧ ПО ДИНАМИЧЕСКОМУ ПРОГРАММИРОВАНИЮ")
    print("="*60)
    
    while True:
        print("\nВыберите задачу для решения:")
        print("1 - Распределение средств между предприятиями")
        print("2 - Кратчайший путь от 1 до 10")
        print("0 - Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "1":
            zadacha_1()
        elif choice == "2":
            zadacha_2()
        elif choice == "0":
            print("\nДо свидания!")
            break
        else:
            print("\nНеверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()