import random
import math

def circle_square_mk(r, n):
    count_inside_circle = 0

    # Генерация n случайных точек в квадрате [-r, r] x [-r, r]
    for _ in range(n):
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)

        # Проверяем, лежит ли точка внутри окружности
        if x**2 + y**2 <= r**2:
            count_inside_circle += 1

    # Площадь квадрата со стороной 2r
    square_area = (2 * r) ** 2

    # Доля точек, попавших внутрь окружности
    fraction_inside_circle = count_inside_circle / n

    # Приближённая площадь окружности
    circle_area = fraction_inside_circle * square_area
    return circle_area


# Тестирование функции
if __name__ == "__main__":
    radius = 5  # Радиус окружности
    experiments = 100000  # Количество экспериментов

    monte_carlo_area = circle_square_mk(radius, experiments)

    # Точная площадь окружности
    exact_area = math.pi * radius ** 2

    # Оценка погрешности
    error = abs(monte_carlo_area - exact_area) / exact_area * 100

    # Результаты
    print(f"Радиус окружности: {radius}")
    print(f"Количество экспериментов: {experiments}")
    print(f"Вычисленная площадь (Монте-Карло): {monte_carlo_area}")
    print(f"Точная площадь: {exact_area}")
    print(f"Погрешность: {error:.5f}%")
