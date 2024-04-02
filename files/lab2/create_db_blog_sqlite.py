import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('db_blog.sqlite3')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Создание таблицы Blog
cursor.execute("""
CREATE TABLE IF NOT EXISTS blog_blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE,
    tagline TEXT
);"""
               )

# Создание таблицы Author
cursor.execute("""
CREATE TABLE IF NOT EXISTS blog_author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200),
    email VARCHAR(254) UNIQUE
);""")

# Создание таблицы AuthorProfile
cursor.execute("""
CREATE TABLE IF NOT EXISTS blog_authorprofile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER UNIQUE,
    bio TEXT,
    phone_number VARCHAR(12) UNIQUE,
    city VARCHAR(120),
    FOREIGN KEY (author_id) REFERENCES blog_author(id)
);""")

# Создание таблицы Entry
cursor.execute("""
CREATE TABLE IF NOT EXISTS blog_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id INTEGER,
    headline VARCHAR(255),
    body_text TEXT,
    pub_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    mod_date DATE DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER,
    number_of_comments INTEGER DEFAULT 0,
    number_of_pingbacks INTEGER DEFAULT 0,
    rating FLOAT DEFAULT 0.0,
    FOREIGN KEY (blog_id) REFERENCES blog_blog(id),
    FOREIGN KEY (author_id) REFERENCES blog_author(id)
);""")

# Создание таблицы Tag
cursor.execute("""
CREATE TABLE IF NOT EXISTS blog_tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE,
    slug_name VARCHAR(50) UNIQUE
);""")


# Создание таблицы для связи многие-ко-многим между Entry и Tag
cursor.execute("""
CREATE TABLE IF NOT EXISTS blog_entry_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (entry_id) REFERENCES blog_entry(id),
    FOREIGN KEY (tag_id) REFERENCES blog_tag(id)
);""")

# Закрытие соединения
conn.close()