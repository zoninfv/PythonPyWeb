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
