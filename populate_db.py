import sqlite3
import random
from math import sqrt, sin, cos, pi

def generate_sample_problems(count=10000):
    """Генерация тестовых математических задач"""
    problems = []

    for i in range(count):
        # Линейные уравнения
        a = random.randint(1, 20)
        b = random.randint(-50, 50)
        c = random.randint(-100, 100)
        problem = f"{a}x + {b} = {c}"
        solution = f"x = {(c - b) / a}"
        problems.append(('linear_equation', problem, solution, random.randint(1, 3)))

        # Квадратные уравнения
        a2 = random.randint(1, 10)
        b2 = random.randint(-20, 20)
        c2 = random.randint(-50, 50)
        discriminant = b2**2 - 4*a2*c2
        if discriminant >= 0:
            x1 = (-b2 + sqrt(discriminant)) / (2*a2)
            x2 = (-b2 - sqrt(discriminant)) / (2*a2)
            solution = f"x₁ = {x1:.2f}, x₂ = {x2:.2f}"
        else:
            solution = "Корней нет (D < 0)"
        problem = f"{a2}x² + {b2}x + {c2} = 0"
        problems.append(('quadratic_equation', problem, solution, random.randint(2, 4)))

        # Тригонометрия
        angle = random.choice([0, 30, 45, 60, 90, 180, 270, 360])
        radians = angle * pi / 180
        problem = f"sin({angle}°) + cos({angle}°)"
        solution = f"{sin(radians) + cos(radians):.4f}"
        problems.append(('trigonometry', problem, solution, random.randint(3, 5)))

    return problems

def populate_database():
    conn = sqlite3.connect('math_bot.db', timeout=20.0)
    cursor = conn.cursor()

    # Вставляем данные партиями для производительности
    batch_size = 1000
    total_inserted = 0

    try:
        for i in range(0, 10000, batch_size):  # 10 000 записей для примера
            batch = generate_sample_problems(batch_size)
            cursor.executemany('''
                INSERT OR IGNORE INTO math_problems
                (problem_type, problem_text, solution_text, difficulty_level)
                VALUES (?, ?, ?, ?)
            ''', batch)
            conn.commit()
            total_inserted += len(batch)
            print(f"Вставлено {total_inserted} записей...")

    except Exception as e:
        print(f"Ошибка при заполнении БД: {e}")
    finally:
        conn.close()

    print(f"База данных заполнена успешно! Всего записей: {total_inserted}")

if __name__ == '__main__':
    populate_database()
