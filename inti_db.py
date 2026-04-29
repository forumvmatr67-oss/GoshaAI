import sqlite3

def create_database():
    conn = sqlite3.connect('math_bot.db')
    cursor = conn.cursor()
  
    # Таблица для математических задач и ответов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS math_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_type TEXT NOT NULL,
            problem_text TEXT UNIQUE NOT NULL,
            solution_text TEXT NOT NULL,
            difficulty_level INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Индекс для быстрого поиска по типу задачи
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_problem_type ON math_problems(problem_type)')
    # Индекс для поиска по тексту задачи
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_problem_text ON math_problems(problem_text)')

    conn.commit()
    conn.close()
    print("База данных создана успешно!")

if __name__ == '__main__':
    create_database()
