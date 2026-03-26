import numpy as np

def solve_mixed_strategies(matrix):
    A = np.array(matrix, dtype=float)
    n = A.shape[0]
    
    row_mins = np.min(A, axis=1)
    col_maxs = np.max(A, axis=0)
    
    max_row_min = np.max(row_mins)
    min_col_max = np.min(col_maxs)
    
    if abs(max_row_min - min_col_max) < 1e-10:
        print(f"Седловая точка найдена! Цена игры: {max_row_min}")
        return None
    
    print("Седловая точка отсутствует. Ищем смешанные стратегии...")
    
    M = np.zeros((n+1, n+1))
    b = np.zeros(n+1)
    
    for j in range(n):
        for i in range(n):
            M[j, i] = A[i, j]
        M[j, n] = -1
    
    for i in range(n):
        M[n, i] = 1
    M[n, n] = 0
    b[n] = 1
    
    try:
        solution = np.linalg.solve(M, b)
        p = solution[:n]
        v = solution[n]
        
        print(f"\nЦена игры: {v:.4f}")
        print(f"Стратегии игрока A: {p}")
        print(f"Проверка sum(p) = {np.sum(p):.4f}")
        
        if np.all(p >= -1e-10):
            print("Все p_i ≥ 0 ")
        else:
            print("Некоторые p_i < 0 → нужно решать задачу линейного программирования")
        
    except np.linalg.LinAlgError:
        print("Матрица вырождена, используем метод последовательных приближений")
        return solve_by_iteration(A)
    
    M2 = np.zeros((n+1, n+1))
    b2 = np.zeros(n+1)
    
    for i in range(n):
        for j in range(n):
            M2[i, j] = A[i, j]
        M2[i, n] = -1
    
    for j in range(n):
        M2[n, j] = 1
    M2[n, n] = 0
    b2[n] = 1
    
    try:
        solution2 = np.linalg.solve(M2, b2)
        q = solution2[:n]
        
        print(f"\nСтратегии игрока B: {q}")
        print(f"Проверка sum(q) = {np.sum(q):.4f}")
        
        if np.all(q >= -1e-10):
            print("Все q_j ≥ 0 ")
        else:
            print("Некоторые q_j < 0 → нужно решать задачу линейного программирования")
        
        return p, q, v
        
    except np.linalg.LinAlgError:
        print("Матрица вырождена")
        return None

def solve_by_iteration(A, max_iter=1000, tol=1e-6):
    n = A.shape[0]
    
    p = np.ones(n) / n
    q = np.ones(n) / n
    
    for iteration in range(max_iter):
        p_old = p.copy()
        q_old = q.copy()
        
        payoffs_A = A @ q_old
        best_response_A = np.argmax(payoffs_A)
        p = np.zeros(n)
        p[best_response_A] = 1
        
        payoffs_B = p_old @ A
        best_response_B = np.argmin(payoffs_B)
        q = np.zeros(n)
        q[best_response_B] = 1
        
        alpha = 2.0 / (iteration + 3)
        p = alpha * p + (1 - alpha) * p_old
        q = alpha * q + (1 - alpha) * q_old
        
        if np.linalg.norm(p - p_old) < tol and np.linalg.norm(q - q_old) < tol:
            print(f"\nСходимость достигнута за {iteration+1} итераций")
            break
    
    v = np.min(p @ A)
    
    print(f"\nЦена игры (приблизительно): {v:.4f}")
    print(f"Стратегии игрока A: {p}")
    print(f"Стратегии игрока B: {q}")
    
    return p, q, v

def solve_lp_simplex(matrix):
    A = np.array(matrix, dtype=float)
    n = A.shape[0]
    
    print("\n" + "="*50)
    print("Решение через линейное программирование")
    print("="*50)
    
    try:
        from scipy.optimize import linprog
        print("Примечание: для полноценного LP-решения рекомендуется scipy.optimize")
        print("Возвращаем приближенное решение методом итераций...")
        return solve_by_iteration(A)
    except ImportError:
        print("scipy.optimize недоступен, используем метод итераций")
        return solve_by_iteration(A)

if __name__ == "__main__":
    matrix = [
        [-1, 3, 2],
        [4, 0, -2],
        [1, 2, -1]
    ]
    
    print("Матрица игры:")
    for row in matrix:
        print(row)
    
    row_mins = [min(row) for row in matrix]
    print(f"\nМинимальные в строках: {row_mins}")
    print(f"Максимин (нижняя цена игры): {max(row_mins)}")
    
    col_maxs = [max(matrix[i][j] for i in range(3)) for j in range(3)]
    print(f"Максимальные в столбцах: {col_maxs}")
    print(f"Минимакс (верхняя цена игры): {min(col_maxs)}")
    
    if max(row_mins) == min(col_maxs):
        saddle_value = max(row_mins)
        print(f"\n✓ Седловая точка найдена! Цена игры: {saddle_value}")
    else:
        print(f"\n✗ Седловая точка отсутствует (maxmin ≠ minimax)")
        
        result = solve_mixed_strategies(matrix)
        
        if result is None:
            print("\nПробуем альтернативный метод...")
            solve_lp_simplex(matrix)