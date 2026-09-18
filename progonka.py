import time

start_total = time.perf_counter()

n = 2**10  # число разбиений

# Входные параметры задачи
k = 12.0  # коэффициент k
q = 5.0  # коэффициент q
l = 1.0  # длина отрезка [0, l]
mu1 = 10.0  # граничное условие слева: u(0)
mu2 = 100.0  # граничное условие справа: u(l)

# Запись в файл
isWriteToFile = 1

def u_exact(x):
    """Точное решение уравнения"""
    return 10.0 + 90.0 * x**2


def f(x):
    """Исходное уравнение: f(x) = -k*u'' + q*u"""
    return -2110.0 + 450.0 * x**2


h = l / n
A = k / (h**2)
B = k / (h**2)
C = 2.0 * k / (h**2) + q

start_solve = time.perf_counter()

a = [0.0] * (n + 1)
b = [0.0] * (n + 1)

a[1] = 0.0
b[1] = mu1

for i in range(1, n):
    delitel = C - A * a[i]
    a[i + 1] = B / delitel
    b[i + 1] = (f(i * h) + A * b[i]) / delitel

# Обратный ход
v = [0.0] * (n + 1)
v[n] = mu2

for i in range(n - 1, -1, -1):
    v[i] = a[i + 1] * v[i + 1] + b[i + 1]

time_solve = (time.perf_counter() - start_solve) * 1000.0

# Таблица 
print(
    f"{'i':>3} | {'x_i':>6} | {'Числ. (v_i)':>12} | {'Точн. (u_i)':>12} | "
    f"{'Погрешность':>12} | {'Невязка':>12}"
)
print("-" * 73)

max_error = 0.0
max_residual = 0.0

with open("output.txt", "w", encoding="utf-8") as out:
    if isWriteToFile:
        out.write(
            "Индекс(i)\tУзел(xi)\tЧисл.реш(vi)\tТочн.реш(ui)\t"
            "Погрешность|vi-ui|\tНевязка(ri)\n"
        )
        out.write("-" * 86 + "\n")

    for i in range(n + 1):
        xi = i * h
        ui = u_exact(xi)
        err = abs(v[i] - ui)

        # Невязка
        if i == 0:
            res = abs(v[0] - mu1)
        elif i == n:
            res = abs(v[n] - mu2)
        else:
            res = abs(A * v[i - 1] - C * v[i] + B * v[i + 1] + f(xi))

        if err > max_error:
            max_error = err
        if res > max_residual:
            max_residual = res

        # Первые 10
        if i <= 10:
            print(
                f"{i:3d} | {xi:6.2f} | {v[i]:12.6f} | {ui:12.6f} | "
                f"{err:12.4e} | {res:12.4e}"
            )

        # Запись в output.txt
        if isWriteToFile:
            out.write(
                f"{i}\t{xi:.10f}\t{v[i]:.10f}\t{ui:.10f}\t"
                f"{err:.10f}\t{res:.10f}\n"
            )

time_total = (time.perf_counter() - start_total) * 1000.0

print("-" * 73)
print(f"Максимальная погрешность: {max_error:.6e}")
print(f"Максимальная невязка:    {max_residual:.6e}")
print(f"Время решения (прогонка): {time_solve:.6f} ms")
print(f"Общее время выполнения:   {time_total:.6f} ms")
if isWriteToFile: print("\nСохранено в файл output.txt")
