import sqlite3
import re

class MathSolver:
    def __init__(self, db_path='math_bot.db'):
        self.db_path = db_path

    def search_solution(self, query):
        """Поиск решения в базе данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Ищем точное совпадение
        cursor.execute(
            "SELECT solution_text FROM math_problems WHERE problem_text = ?",
            (query,)
        )
        result = cursor.fetchone()

        if result:
            conn.close()
            return result[0]

        # Поиск по частичному совпадению
        cursor.execute(
            "SELECT solution_text FROM math_problems WHERE problem_text LIKE ? LIMIT 1",
            (f"%{query}%",)
        )
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def get_random_problem(self, problem_type=None):
        """Получение случайной задачи"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if problem_type:
            cursor.execute(
                "SELECT problem_text, solution_text FROM math_problems WHERE problem_type = ? ORDER BY RANDOM() LIMIT 1",
                (problem_type,)
            )
        else:
            cursor.execute(
                "SELECT problem_text, solution_text FROM math_problems ORDER BY RANDOM() LIMIT 1"
            )

        result = cursor.fetchone()
        conn.close()

        return result if result else ("Задача не найдена", "Решение не найдено")
