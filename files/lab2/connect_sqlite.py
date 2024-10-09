import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('db.sqlite3')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Выполнение SQL-запросов
cursor.execute("SELECT * FROM db_train_alternative_entry")
rows = cursor.fetchall()
print(rows)


# Закрытие соединения
conn.close()