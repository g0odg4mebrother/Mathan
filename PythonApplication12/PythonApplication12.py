import logging
import time
import math
import sys

class MathSolverApp:
    def __init__(self):
        logging.basicConfig(
            filename='log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
    def log_operation(self, operation_name, input_data, result):
        self.logger.info(f"Операция: {operation_name}, Входные данные: {input_data}, Результат: {result}")
    
    def log_error(self, operation_name, error_message):
        self.logger.error(f"Операция: {operation_name}, Ошибка: {error_message}")
    
    def measure_time(self, func, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time

    def solve_linear_equation(self, a, b, c):
        assert isinstance(a, int), "Коэффициент a должен быть целым числом"
        assert isinstance(b, int), "Коэффициент b должен быть целым числом" 
        assert isinstance(c, int), "Коэффициент c должен быть целым числом"
        assert c != 0, "Знаменатель c не может быть равен нулю"
        
        if a == 0:
            if b == 0:
                return "Бесконечное множество решений (0 = 0)"
            else:
                if b % c == 0:
                    return "Нет решений (числитель не равен 0)"
                else:
                    return "Нет целочисленных решений"
        
        if (-b) % a != 0:
            return "Нет целочисленных решений"
        
        x = -b // a
        
        if (a * x + b) % c == 0:
            return f"x = {x}"
        else:
            return "Нет целочисленных решений"
    
    def task1(self):
        print("\n" + "="*50)
        print("ЗАДАНИЕ 1: Решение уравнения (ax + b)/c = 0 в целых числах")
        print("="*50)
        
        try:
            a = int(input("Введите целое число a: "))
            b = int(input("Введите целое число b: "))
            c = int(input("Введите целое число c (c ≠ 0): "))
            
            input_data = f"a={a}, b={b}, c={c}"
            
            result, exec_time = self.measure_time(self.solve_linear_equation, a, b, c)
            
            print(f"\nРезультат: {result}")
            print(f"Время выполнения: {exec_time:.6f} секунд")
            
            self.log_operation("Линейное уравнение", input_data, f"{result}, время: {exec_time:.6f}с")
            
        except AssertionError as e:
            print(f"Ошибка: {e}")
            self.log_error("Линейное уравнение", str(e))
        except ValueError:
            print("Ошибка: Введены некорректные данные. Ожидаются целые числа.")
            self.log_error("Линейное уравнение", "Некорректный ввод данных")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            self.log_error("Линейное уравнение", f"Неожиданная ошибка: {e}")

    def classify_triangle(self, a, b, c):
        assert a > 0 and b > 0 and c > 0, "Стороны треугольника должны быть положительными числами"
        assert a + b > c and a + c > b and b + c > a, "Треугольник с такими сторонами не существует"
        
        sides = sorted([a, b, c])
        a, b, c = sides[0], sides[1], sides[2]
        
        if a == b == c:
            side_type = "Равносторонний"
        elif a == b or b == c or a == c:
            side_type = "Равнобедренный"
        else:
            side_type = "Разносторонний"
        
        if abs(a*a + b*b - c*c) < 1e-10:
            angle_type = "Прямоугольный"
        elif a*a + b*b > c*c:
            angle_type = "Остроугольный"
        else:
            angle_type = "Тупоугольный"
        
        p = (a + b + c) / 2
        area = math.sqrt(p * (p - a) * (p - b) * (p - c))
        
        return side_type, angle_type, area
    
    def task2(self):
        print("\n" + "="*50)
        print("ЗАДАНИЕ 2: Определение вида треугольника и его площади")
        print("="*50)
        
        try:
            a = float(input("Введите длину стороны a: "))
            b = float(input("Введите длину стороны b: "))
            c = float(input("Введите длину стороны c: "))
            
            input_data = f"a={a}, b={b}, c={c}"
            
            result, exec_time = self.measure_time(self.classify_triangle, a, b, c)
            side_type, angle_type, area = result
            
            print(f"\nВид треугольника:")
            print(f"  По сторонам: {side_type}")
            print(f"  По углам: {angle_type}")
            print(f"  Площадь: {area:.3f} квадратных единиц")
            print(f"\nВремя выполнения: {exec_time:.6f} секунд")
            
            result_str = f"{side_type}, {angle_type}, площадь={area:.3f}"
            self.log_operation("Треугольник", input_data, f"{result_str}, время: {exec_time:.6f}с")
            
        except AssertionError as e:
            print(f"Ошибка: {e}")
            self.log_error("Треугольник", str(e))
        except ValueError:
            print("Ошибка: Введены некорректные данные. Ожидаются числа.")
            self.log_error("Треугольник", "Некорректный ввод данных")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            self.log_error("Треугольник", f"Неожиданная ошибка: {e}")

    def solve_quadratic(self, a, b, c):
        assert isinstance(a, int), "Коэффициент a должен быть целым числом"
        assert isinstance(b, int), "Коэффициент b должен быть целым числом"
        assert isinstance(c, int), "Коэффициент c должен быть целым числом"
        
        if a == 0:
            if b == 0:
                if c == 0:
                    return "Бесконечное множество решений (0 = 0)"
                else:
                    return "Нет решений"
            else:
                if c % b == 0:
                    return f"x = {-c // b} (линейное уравнение)"
                else:
                    return "Нет целочисленных решений (линейное уравнение)"
        
        D = b*b - 4*a*c
        
        if D < 0:
            return "Нет действительных корней"
        
        sqrt_D = int(math.isqrt(D)) if D >= 0 else 0
        if sqrt_D * sqrt_D != D:
            return "Дискриминант не является полным квадратом, корни не целые"
        
        x1_numerator = -b + sqrt_D
        x2_numerator = -b - sqrt_D
        
        solutions = []
        
        if x1_numerator % (2*a) == 0:
            x1 = x1_numerator // (2*a)
            solutions.append(x1)
        
        if D > 0 and x2_numerator % (2*a) == 0:
            x2 = x2_numerator // (2*a)
            if len(solutions) == 0 or x2 != solutions[0]:
                solutions.append(x2)
        
        if len(solutions) == 0:
            return "Нет целочисленных корней"
        elif len(solutions) == 1:
            return f"x = {solutions[0]}"
        else:
            return f"x1 = {solutions[0]}, x2 = {solutions[1]}"
    
    def task3(self):
        print("\n" + "="*50)
        print("ЗАДАНИЕ 3: Решение квадратного уравнения ax² + bx + c = 0 в целых числах")
        print("="*50)
        
        try:
            a = int(input("Введите целое число a (коэффициент при x²): "))
            b = int(input("Введите целое число b (коэффициент при x): "))
            c = int(input("Введите целое число c (свободный член): "))
            
            input_data = f"a={a}, b={b}, c={c}"
            
            result, exec_time = self.measure_time(self.solve_quadratic, a, b, c)
            
            print(f"\nРезультат: {result}")
            print(f"Время выполнения: {exec_time:.6f} секунд")
            
            self.log_operation("Квадратное уравнение", input_data, f"{result}, время: {exec_time:.6f}с")
            
        except AssertionError as e:
            print(f"Ошибка: {e}")
            self.log_error("Квадратное уравнение", str(e))
        except ValueError:
            print("Ошибка: Введены некорректные данные. Ожидаются целые числа.")
            self.log_error("Квадратное уравнение", "Некорректный ввод данных")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            self.log_error("Квадратное уравнение", f"Неожиданная ошибка: {e}")

    def run(self):
        while True:
            print("\n" + "="*50)
            print("ГЛАВНОЕ МЕНЮ")
            print("="*50)
            print("1. Решение линейного уравнения (ax + b)/c = 0")
            print("2. Определение вида треугольника и его площади")
            print("3. Решение квадратного уравнения ax² + bx + c = 0")
            print("4. Выход")
            print("-"*50)
            
            choice = input("Выберите задание (1-4): ").strip()
            
            if choice == '1':
                self.task1()
            elif choice == '2':
                self.task2()
            elif choice == '3':
                self.task3()
            elif choice == '4':
                print("\nСпасибо за использование приложения!")
                self.logger.info("Программа завершена пользователем")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")
            
            input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    app = MathSolverApp()
    
    app.logger.info("="*50)
    app.logger.info("ПРОГРАММА ЗАПУЩЕНА")
    app.logger.info("="*50)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        app.logger.info("Программа прервана пользователем (Ctrl+C)")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        app.logger.error(f"Критическая ошибка: {e}")
    finally:
        app.logger.info("="*50)
        app.logger.info("ПРОГРАММА ЗАВЕРШЕНА")
        app.logger.info("="*50)