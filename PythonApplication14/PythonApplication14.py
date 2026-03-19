import numpy as np

def sistema(x, y):
    return np.array([y[1], 2*np.exp(x) + np.exp(2*x) - np.exp(x)*y[1] - y[0]])

def rk4(f, a, b, y0, n):
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = np.zeros((n+1, len(y0)))
    y[0] = y0
    
    for i in range(n):
        k1 = f(x[i], y[i])
        k2 = f(x[i] + h/2, y[i] + h/2 * k1)
        k3 = f(x[i] + h/2, y[i] + h/2 * k2)
        k4 = f(x[i] + h, y[i] + h * k3)
        y[i+1] = y[i] + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    
    return x, y

def strelba(target, eps=1e-10, max_it=100):
    s_left, s_right = 0.0, 5.0
    n = 100
    
    _, y1 = rk4(sistema, 0, 1, [1, s_left], n)
    _, y2 = rk4(sistema, 0, 1, [1, s_right], n)
    y1_end, y2_end = y1[-1,0], y2[-1,0]
    
    print("Поиск начальной производной:")
    print(f"  y'(0) = {s_left:.4f} -> y(1) = {y1_end:.8f}")
    print(f"  y'(0) = {s_right:.4f} -> y(1) = {y2_end:.8f}")
    print(f"  Требуется y(1) = {target:.8f}")
    print("-"*50)
    
    for i in range(max_it):
        if abs(y2_end - y1_end) < 1e-12:
            break
            
        s_new = s_right - (y2_end - target) * (s_right - s_left) / (y2_end - y1_end)
        
        x_new, y_new = rk4(sistema, 0, 1, [1, s_new], n)
        y_new_end = y_new[-1,0]
        
        print(f"Шаг {i+1}: y'(0) = {s_new:.8f} -> y(1) = {y_new_end:.8f}, error = {abs(y_new_end - target):.2e}")
        
        if abs(y_new_end - target) < eps:
            print(f"\nНайдено за {i+1} итераций")
            return x_new, y_new, s_new
            
        s_left, s_right = s_right, s_new
        y1_end, y2_end = y2_end, y_new_end
    
    return x_new, y_new, s_new

target = np.exp(1)
x, y, s_opt = strelba(target)

print("\n" + "="*70)
print("РЕЗУЛЬТАТЫ РЕШЕНИЯ")
print("="*70)
print(f"Уравнение: y'' + e^x*y' + y = 2e^x + e^(2x)")
print(f"Условия: y(0)=1, y(1)=e")
print(f"y'(0) = {s_opt:.8f}")
print("="*70)

print("\nТАБЛИЦА ЗНАЧЕНИЙ:")
print("-"*60)
print("     x     |      y(x)      |     y'(x)     |   погрешность")
print("-"*60)

for i in range(0, len(x), len(x)//15):
    err = abs(y[i,0] - target) if abs(x[i]-1) < 0.01 else 0
    if err > 0:
        print(f"{x[i]:10.4f} | {y[i,0]:14.8f} | {y[i,1]:14.8f} | {err:12.2e}")
    else:
        print(f"{x[i]:10.4f} | {y[i,0]:14.8f} | {y[i,1]:14.8f} |     -")

print("-"*60)
print(f"\nПроверка:")
print(f"  y(0) = {y[0,0]:.8f} (требуется 1)")
print(f"  y(1) = {y[-1,0]:.8f} (требуется e = {target:.8f})")
print(f"  Ошибка = {abs(y[-1,0]-target):.2e}")

print("\n" + "="*70)
print("ИССЛЕДОВАНИЕ ТОЧНОСТИ")
print("="*70)
print("   h    |     y(1)     |   ошибка   | порядок")
print("-"*60)

h_vals = [0.1, 0.05, 0.02, 0.01, 0.005]
prev_err = None

for h in h_vals:
    n = int(1/h)
    _, yy = rk4(sistema, 0, 1, [1, s_opt], n)
    err = abs(yy[-1,0] - target)
    
    if prev_err is None:
        print(f"{h:7.3f} | {yy[-1,0]:12.8f} | {err:9.2e} |    -")
    else:
        p = np.log2(prev_err/err)
        print(f"{h:7.3f} | {yy[-1,0]:12.8f} | {err:9.2e} | {p:6.2f}")
    
    prev_err = err

print("="*70)