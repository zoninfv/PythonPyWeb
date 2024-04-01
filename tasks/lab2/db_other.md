
## 1. Подключение к SQLite БД через встроенный модуль sqlite3

Про модуль можно почитать в [документации Python](https://docs.python.org/3/library/sqlite3.html)

В корне проекта создайте файл `connect_sqlite.py` в нём подключимся и сделаем пару запросов

В файле пропишите

```python
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('db.sqlite3')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Выполнение SQL-запроса
cursor.execute("SELECT * FROM db_train_alternative_entry")  # Выполняем запрос
rows = cursor.fetchall()  # Получаем данные
print(rows)  # Печатаем данные. 
# Заметьте возвращаться только список значений из базы данных, не объект как в случае с ORM. Это аналогично 
# выполнению команды values_list() в Django ORM.


# Закрытие соединения
conn.close()
```

В общем случае выполняются следующие команды (в зависимости от задач):

#### 1. Подключение к БД и получения ссылки на это подключение (`db.sqlite3` название БД к которой идёт подключение)

```python
conn = sqlite3.connect('db.sqlite3')
```

#### 2. Получение курсора (объекта для работы с запросами)

```python
cursor = conn.cursor()
```

#### 3. Создание запроса в БД. Все они делаются через `execute`, где прописывается SQL код. 
Общие выполняемые задачи:

* ***Создание таблицы*** с названием `table_name` и полями `id`, `name`

```python
cursor.execute('''CREATE TABLE IF NOT EXISTS table_name (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL)''')
```

* ***Удаление таблицы*** `table_name`

```python
cursor.execute("DROP TABLE IF EXISTS table_name")
```

* ***Добавление поля*** `new_column_name` в таблицу `table_name`

```python
cursor.execute("ALTER TABLE table_name ADD COLUMN new_column_name INTEGER")
```

* ***Удаление поля*** `column_name` из таблицы `table_name`

```python
cursor.execute("ALTER TABLE table_name DROP COLUMN column_name")
```

* ***Получение данных*** (для примера всех полей таблицы `table_name`) 

```python
cursor.execute("SELECT * FROM table_name")
```

Однако, чтобы отобразить полученные данные, необходимо затем вызвать один из методов `fetchone()`, `fetchall()` 
или `fetchmany(size)`:

* `fetchone()`:

  * Возвращает следующий ряд результатов запроса.
  * Если рядов больше нет, возвращает None.
  * Используется, когда ожидается получение только одной строки результата.

```python
# Получить первый ряд
row = cursor.fetchone()
```

* `fetchall()`:

  * Возвращает список всех строк результатов запроса.
  * Если рядов нет, возвращает пустой список [].
  * Используется, когда нужны все строки результата, и их количество не очень велико.

```python
# Получить все ряды
rows = cursor.fetchall()
```

* `fetchmany(size)`:

  * Возвращает список строк размером size.
  * Если рядов больше нет, возвращает пустой список [].
  * Используется, когда нужно получить только часть результатов, особенно если количество строк велико.

```python
# Получить первые 5 рядов
rows = cursor.fetchmany(5)
```

* ***Вставка данных*** (в таблицу `table_name` за счёт параметризованных запросов)

```python
cursor.execute("INSERT INTO table_name (name) VALUES (?)", ('John',))
conn.commit()  # Фиксация изменений, чтобы закрыть транзакцию
# conn.rollback() # Чтобы отменить транзакцию
```


* ***Обновление данных*** (в строке с `id`=1 таблицы `table_name`)

```python
cursor.execute("UPDATE table_name SET name = ? WHERE id = ?", ('Alice', 1))
conn.commit()  # Фиксация изменений, чтобы закрыть транзакцию
# conn.rollback() # Чтобы отменить транзакцию
```

* ***Удаление данных*** (строки с `id`=1 из таблицы `table_name`)

```python
cursor.execute("DELETE FROM table_name WHERE id = ?", (1,))
conn.commit()  # Фиксация изменений, чтобы закрыть транзакцию
# conn.rollback() # Чтобы отменить транзакцию
```

#### 4. Закрытие соединения, с использованием команды `close()`. 

```python
# Закрытие соединения
conn.close()
```

Закрытие соединения с базой данных **важно по нескольким причинам**:

* `Освобождение ресурсов`: Когда вы закрываете соединение, вы освобождаете ресурсы, занятые этим соединением, такие как сетевые ресурсы и память сервера базы данных. 
Это позволяет вашему приложению эффективно управлять ресурсами и избежать утечек памяти.

* `Сброс состояния`: При закрытии соединения состояние транзакции сбрасывается, что позволяет гарантировать целостность 
данных и избежать нежелательных эффектов от предыдущих операций.

* `Предотвращение блокировки`: Долгое открытое соединение может привести к блокировке ресурсов базы данных, особенно 
в многопользовательской среде. Закрытие соединения после использования позволяет другим клиентам получить доступ к заблокированным ресурсам.

* `Улучшение производительности`: Закрытие соединения также может повысить производительность базы данных, 
освобождая ресурсы сервера для обработки других запросов.

* `Избежание утечек соединений`: Если соединение не закрывается явно, оно может оставаться открытым в случае возникновения 
исключения или ошибки в коде. Это может привести к исчерпанию пула соединений и проблемам производительности.


## 2. Пример создания и наполнения БД SQLite только через модуль sqlite3

Воссоздадим наиболее близкие таблицы имеющегося приложения `db_train_alternative`

Создадим файл в корне проекта `create_db_blog_sqlite.py`

И в этот файл скопируйте код, выполните этот код

```python
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
```

Теперь у вас в корне проекта появилась база `db_blog.sqlite3` со структурой, но без наполнения. Наполним эту базу.

В корне проекта создайте `fill_db_blog_sqlite.py`, перенесите туда этот код и запустите.

```python
import sqlite3
from datetime import datetime

# Подключение к базе данных SQLite
conn = sqlite3.connect('db_blog.sqlite3')
cursor = conn.cursor()

# Заполнение таблицы Blog
cursor.execute("INSERT INTO blog_blog (name, tagline) VALUES (?, ?)", ('Пример блога', 'Просто пример блога'))
blog_id = cursor.lastrowid  # Получение id только что добавленной строки

# Заполнение таблицы Author
cursor.execute("INSERT INTO blog_author (name, email) VALUES (?, ?)", ('Иван Иванов', 'ivan@example.com'))
author_id = cursor.lastrowid  # Получение id только что добавленной строки

# Заполнение таблицы AuthorProfile
cursor.execute("INSERT INTO blog_authorprofile (author_id, bio, phone_number, city) VALUES (?, ?, ?, ?)", (author_id, 'Lorem ipsum dolor sit amet', '+79123456789', 'Москва'))

# Заполнение таблицы Entry
cursor.execute("INSERT INTO blog_entry (blog_id, headline, body_text, pub_date, mod_date, author_id, number_of_comments, number_of_pingbacks, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (blog_id, 'Первая запись', 'Это первая запись', datetime.now(), datetime.now(), author_id, 0, 0, 0.0))

# Заполнение таблицы Tag
cursor.execute("INSERT INTO blog_tag (name, slug_name) VALUES (?, ?)", ('Пример тега', 'primer-tega'))

# Получение идентификаторов вставленных строк
entry_id = cursor.lastrowid  # Получение id только что добавленной строки
tag_id = cursor.lastrowid  # Получение id только что добавленной строки

# Заполнение таблицы для связи многие-ко-многим между Entry и Tag
cursor.execute("INSERT INTO blog_entry_tags (entry_id, tag_id) VALUES (?, ?)", (entry_id, tag_id))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
```

Теперь наша БД заполнена минимальными данными. Можете проверить данную БД через обозреватель базы данных, допустим такую как
`PostgreSQL` (пробовать посмотреть через Django не выйдет, так как Django даже не знает о существовании данной базы).

## 3. Подключение к PosgreSQL через модуль psycopg2

Для подключения необходимо скачать модуль `psycopg2`. Официальная [документация](https://www.psycopg.org/docs/) 

```python
pip install psycopg2
```

Для, `psycopg2`, так же как и `sqlite3`, предоставляет интерфейс для выполнения SQL-запросов и манипуляции с базой данных в Python. 
Обе библиотеки предоставляют объект курсора, с помощью которого можно выполнять SQL-запросы, получать результаты и управлять транзакциями. 

Основные сходства между `psycopg2` и `sqlite3`:

1. `Подключение к базе данных`: Обе библиотеки предоставляют функции для подключения к базе данных через `connect`. 
Например, для `psycopg2` это `psycopg2.connect()`, а для `sqlite3` это `sqlite3.connect()`.

2. `Исполнение SQL-запросов`: Оба модуля позволяют выполнить SQL-запросы с использованием метода `execute()` объекта курсора.

3. `Получение результатов`: Результаты SQL-запросов могут быть получены с помощью методов `fetchone()`, `fetchall()` и `fetchmany()` объекта курсора.

4. `Управление транзакциями`: Каждое выполнение SQL-запроса начинает новую транзакцию, которая может быть закрыта с помощью метода `commit()` для сохранения изменений или отменена с помощью метода `rollback()`.

5. `Закрытие соединения`: Соединение с базой данных должно быть закрыто после завершения работы с ней с помощью метода `close()`.

6. `Параметризованные запросы`: Обе библиотеки поддерживают параметризованные запросы для безопасного выполнения SQL-запросов с использованием значений, которые предоставляются динамически.

7. `Обработка ошибок`: Обе библиотеки предоставляют механизмы для обработки ошибок, возникающих при выполнении запросов или установке соединения с базой данных.

Хотя синтаксис SQL и некоторые функции могут отличаться между разными СУБД, общие концепции работы с базами данных остаются теми же как в `psycopg2`, так и в `sqlite3`.

`psycopg2` и `sqlite3` обе являются библиотеками для работы с базами данных в Python, они предназначены для работы с разными типами СУБД и имеют некоторые различия в функциональности и подходах. 

Основные различия между ними:

1. Типы баз данных:

* `psycopg2`: Предназначен для работы с PostgreSQL.
* `sqlite3`: Предназначен для работы с SQLite.

2. Типы данных:

Обе библиотеки имеют разные наборы типов данных, согласно поддерживаемым типам СУБД. 
Например, типы данных PostgreSQL могут включать UUID, массивы, JSON и другие типы, которых нет в SQLite.

3. Функциональность:

* `psycopg2` обычно предоставляет более широкий спектр функциональности, так как PostgreSQL обладает более богатым набором возможностей и поддерживает более сложные запросы, транзакции, процедуры и т. д.
* `sqlite3` предоставляет простой, легковесный и автономный движок базы данных, который обычно используется для небольших приложений и прототипирования.

4. Подключение:

* `psycopg2` подключается к серверу PostgreSQL, который может работать в клиент-серверной архитектуре, обеспечивая удаленный доступ к базе данных.
* `sqlite3` предоставляет файловую базу данных, которая хранится локально на диске и не требует отдельного сервера.

5. Производительность:

* Обычно `PostgreSQL` и `psycopg2` показывают лучшую производительность при работе с большими объемами данных и многопользовательскими сценариями.
* `SQLite` и `sqlite3` обычно обеспечивают хорошую производительность для небольших приложений и однопользовательских сценариев.

6. Функциональные особенности:

* `psycopg2` может использовать такие возможности PostgreSQL, как генерация UUID, работа с JSON, полнотекстовый поиск, геопространственные запросы и т. д.
* `sqlite3` предоставляет функциональность, специфичную для SQLite, такую как вложенные транзакции, функции для работы с временем и датой, и т. д.

В целом, выбор между `psycopg2` и `sqlite3` зависит от требований вашего проекта, характеристик вашей базы данных и специфики вашего приложения.

## 4. Пример подключения к PosgreSQL через модуль psycopg2

```python
import psycopg2

conn = psycopg2.connect(
        dbname="your_database", 
        user="your_username", 
        password="your_password", 
        host="localhost", 
        port="5432"
    )
```

## 5. Подключение к MySQL через модуль mysql

Для подключения необходимо скачать модуль `mysql-connector-python`. Подробно по подключение и использование можно почитать в [статье](https://proglib.io/p/python-i-mysql-prakticheskoe-vvedenie-2021-01-06)

```python
pip install mysql-connector-python
```

В общем случае, обе библиотеки, `mysql-connector-python` (для работы с MySQL) и `sqlite3`, 
предоставляют схожий функционал для работы с базами данных, но есть некоторые различия, вызванные спецификой каждой СУБД.

Подключение к `MySQL`

```python
import mysql.connector

try:
    # Подключение к базе данных MySQL
    conn = mysql.connector.connect(
        host="localhost", 
        user="your_username", 
        password="your_password", 
        database="your_database"
    )
    
    # Создание объекта курсора
    cursor = conn.cursor()
    
    # Выполнение SQL-запроса
    cursor.execute("SELECT VERSION();")
    
    # Получение результата
    db_version = cursor.fetchone()
    print("Версия сервера MySQL:", db_version)

except mysql.connector.Error as e:
    print("Ошибка при подключении к базе данных MySQL:", e)
finally:
    # Закрытие соединения
    if conn is not None:
        conn.close()
```

## 6. Альтернативные ORM

Django ORM не единственная ORM на python, но единственная оптимизированная под работу с Django.

В Python существует несколько `ORM` (Object-Relational Mapping), которые позволяют работать с базами данных объектно-ориентированным образом, 
преобразуя данные из таблиц базы данных в объекты Python и обратно. 

Некоторые из наиболее популярных ORM для Python включают:

1. `Django ORM`: Встроенный ORM в фреймворк Django. Предоставляет мощные инструменты для работы с базами данных, включая автоматическое создание схемы базы данных, миграции данных, запросы на языке ORM и многое другое.


2. `SQLAlchemy`([документация](https://docs.sqlalchemy.org/en/20/)): SQLAlchemy является одним из самых популярных ORM для Python. Он обеспечивает гибкую и мощную абстракцию для работы с базами данных, поддерживая различные СУБД и предоставляя широкие возможности для создания запросов и выполнения операций с данными.


3. `Peewee`([документация](http://docs.peewee-orm.com/en/latest/index.html)): Peewee - это простая и легковесная ORM для Python, которая обеспечивает простой синтаксис и удобство использования. Она поддерживает различные СУБД и обладает хорошей документацией.


4. `SQLObject`([документация](https://www.sqlobject.org/#documentation)): SQLObject является ORM с открытым исходным кодом, который обеспечивает простой и интуитивно понятный интерфейс для работы с базами данных. Он поддерживает различные СУБД и предоставляет инструменты для создания схемы базы данных, выполнения запросов и манипулирования данными.


5. `Pony ORM`([документация](https://docs.ponyorm.org/)): Pony ORM предоставляет простой и выразительный интерфейс для работы с базами данных. Он поддерживает автоматическое создание схемы базы данных, типизацию данных и создание запросов на языке Python.


Если не разрабатывать на Django, то выбирают чаще всего `SQLAlchemy` как `ORM`, поэтому вкратце её и рассмотрим, так как
она такая же объёмная как `Django ORM`.

## 7. Работа с SQLAlchemy

SQLAlchemy - это популярный ORM (Object-Relational Mapping) для Python, который позволяет работать с базами данных объектно-ориентированным образом. 
SQLAlchemy обеспечивает гибкую и мощную абстракцию для работы с различными СУБД и предоставляет широкие возможности для создания запросов и выполнения операций с данными.

Установка

```python
pip install sqlalchemy
```

Вот основные шаги по работе с SQLAlchemy:

1. `Создание моделей`

Определите классы моделей, которые представляют таблицы в вашей базе данных. Каждый класс модели обычно наследуется 
от базового класса `Base`, который предоставляется `SQLAlchemy`.

Пример:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
```

2. `Создание подключения с базой данных`


```python
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlalchemy.sqlite3')
```

3. `Создание таблиц из моделей`

```python
# Создаем все таблицы, определенные в моделях
Base.metadata.create_all(engine)
```

4. `Создание сессии`

Создайте объект сессии, который представляет собой интерфейс для взаимодействия с базой данных.

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```


5. `Выполнение операций с данными`

Используйте методы сессии для добавления, извлечения, обновления и удаления данных.

Пример добавления записи в таблицу:

```python
new_user = User(name='John', age=30)
session.add(new_user)
session.commit()
```

Пример извлечения данных:

```python
user = session.query(User).filter_by(name='John').first()
print(user.age)
```

6. `Закрытие сессии`

Важно закрывать сессию после завершения работы с базой данных, чтобы освободить ресурсы.

```python
session.close()
```

Тогда полный код будет выглядеть следующим образом (в корне проекта можно создать файл `connect_sqlite_sqlalchemy.py` и наполнить его кодом)

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Создаем базовый класс моделей
class Base(DeclarativeBase):
    pass


# Определяем модель User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


# Создаем соединение с базой данных
engine = create_engine('sqlite:///sqlalchemy.sqlite3')

# Создаем все таблицы, определенные в моделях
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Создаем объект пользователя и добавляем его в сессию
new_user = User(name='John', age=30)
session.add(new_user)

# Фиксируем изменения в базе данных
session.commit()

# Получение данных
user = session.query(User).filter_by(name='John').first()
print(user.age)

# Закрываем сессию
session.close()

```

Это лишь краткое введение в работу с SQLAlchemy. Библиотека обладает обширным функционалом, включая поддержку различных типов запросов, отношений между таблицами, транзакций, миграций и многого другого. 
Если требуется более детальный обзор, то рекомендуется изучить официальную документацию SQLAlchemy.

Более детально про возможности можно прочитать в [ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)

