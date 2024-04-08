## Сериализатор

Сериализаторы можно создать в любом удобном месте в коде вашего проекта, 
но есть ещё подход отнести под них отдельный определенный файл такой как 
`serializers.py`

Сериализатор создаётся как класс наследующийся от базового класса. 

Под базовым классом чаще всего бывает:

* `BaseSerializer` - Является базовым абстрактным классом, от которого наследуются другие сериализаторы в DRF.
Этот класс предоставляет основные функциональные возможности для сериализации и десериализации данных, но он не предоставляет 
никакой конкретной реализации для различных типов данных или моделей. 
**Может понадобиться в случае необходимости создания своего типа сериализатора.** 


* `Serializer` - Является основным классом сериализатора в DRF. Он предоставляет мощные функциональные возможности для 
сериализации и десериализации различных типов данных, включая словари, списки, модели Django и другие.
Serializer используется для создания сериализаторов, которые могут преобразовывать сложные структуры данных в форматы JSON 
или другие форматы для передачи через API.
Этот класс обычно используется для сериализации единичных объектов или сложных структур данных.


* `ListSerializer` - Является специальным классом сериализатора, который предоставляет 
дополнительные возможности для сериализации списков объектов.
Этот класс позволяет определить особое поведение для сериализации списка объектов, 
когда вам нужно производить дополнительные манипуляции с каждым объектом списка.
`ListSerializer` используется для сериализации списков объектов и может быть полезен, 
когда вам нужно контролировать сериализацию элементов списка или добавить дополнительные данные к каждому объекту.


* `ModelSerializer` - Предоставляет простой и удобный способ автоматической сериализации и десериализации моделей Django.
Он обрабатывает все поля модели, включая внешние ключи и связи многие-к-одному или многие-ко-многим.
С помощью ModelSerializer вы можете легко создавать API для вашей модели, которое позволяет выполнять операции CRUD 
(создание, чтение, обновление, удаление) с данными модели.
Кроме того, ModelSerializer автоматически создает валидаторы, основанные на вашей модели, и обрабатывает валидацию данных при десериализации.


* `HyperlinkedModelSerializer` - предоставляет те же функциональные возможности, что и ModelSerializer, но с 
добавленным функционалом гиперссылок (URL-ссылок) для связанных моделей.
Когда используется HyperlinkedModelSerializer, связанные модели представляются в виде URL-ссылок, а не как простые идентификаторы (Primary Keys). 
Это делает представление данных более удобным и навигируемым для клиентов.
При использовании HyperlinkedModelSerializer, клиенты могут получить доступ к 
связанным объектам, следуя гиперссылкам, что упрощает навигацию и обмен данными между различными частями вашего API.
Для работы с HyperlinkedModelSerializer необходимо настроить URL-маршруты для представления гиперссылок.


Базовые классы находятся в `rest_framework.serializers`
```python
from rest_framework.serializers import BaseSerializer, Serializer, \
    ListSerializer, ModelSerializer, HyperlinkedModelSerializer
```

Код сериализаторов можно посмотреть по пути `venv\Lib\site-packages\rest_framework\serializers.py`

### 1. Работа с сериализатором
В общем случае объявление сериализатора выглядит следующим образом:

#### 1.1 Объявление класса сериализатора

Объявляем класс сериализатор, наследуемся от базового класса который нам необходим 
и прописываем внутри необходимые поля для сериализации(по этим полям будут формироваться JSON от объекта).
Ниже приведен урезанный сериализатор для модели Entry что есть в БД. Объекты полей по названию очень похожи с БД, только идут из 
serializers. Параметры которые можно передавать при формировании полей и доступные поля описаны в `fields_serializers.md`

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()
```

#### 1.2 Создание объекта сериализатора

В конструктор сериализатора можно передавать как данные в формате словаря, так и объекты у которых структура совпадает с
определением полей в сериализаторе(поля одинаково названы и похожие типы, чтобы можно было их трансформировать).

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()


# Создаём объект сериализатора
serializer = EntrySerializer()
print(serializer)
"""
EntrySerializer():
    headline = CharField()
    body_text = CharField()
"""
```

Если необходимо передать данные в сериализатор, то это всегда делается через инициализацию.

Есть несколько способов инициализировать сериализатор с данными:
1. Передача данных в словаре с последующей валидацией данных. Для этого объект словаря инициализируется с параметром `data`.
А для дальнейшей сериализации и десериализации необходимо вызвать метод `is_valid()` который запустит механизм валидации
входных данных.
```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()

# Входные данные
data = {'headline': 'headline',
        'body_text': 'body_text'}

# Создаём объект сериализатора
serializer = EntrySerializer(data=data)
print(serializer)
"""
EntrySerializer(data={'headline': 'headline', 'body_text': 'body_text'}):
    headline = CharField()
    body_text = CharField()
"""
# Валидируем входные данные
print(serializer.is_valid())  # True
# Данные готовые для сериализации (формирования JSON)
print(serializer.data)  # {'headline': 'headline', 'body_text': 'body_text'}
# Десериализованные валидированные данные (объекты Python для дальнейного создания или обновления объектов)
print(serializer.validated_data)  # OrderedDict([('headline', 'headline'), ('body_text', 'body_text')])
```

2. Передача объекта у которого атрибуты называются аналогично как и поля сериализатора, это может быть объект БД Django или
любой другой объект Python. На этот раз происходит передача объекта при инициализации и вызов `is_valid()` уже не нужен, так как подразумевается что данные внутри объекта Python валидные. Сериализатор будет
трансформировать только те данные в объекте, поля которых описаны в сериализаторе. 

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()

# Создаём объект сериализатора на базе объекта БД
serializer = EntrySerializer(Entry.objects.get(pk=3))
print(serializer)
"""
EntrySerializer(<Entry: Знакомство с Парижем>):
    headline = CharField()
    body_text = CharField()
"""

# Данные готовые для сериализации (формирования JSON). Хотя в объекте БД много полей, но сериализуются только те, что
# описаны в сериализаторе
print(serializer.data)  # {'headline': 'Знакомство с Парижем',
# 'body_text': 'Париж - город любви, искусства и изысканности. \nЗнакомство с Парижем - это погружение в его узкие
# улочки, исторические \nдостопримечательности и культурную сцену. Прогулка по набережной Сены, \nпосещение Эйфелевой
# башни, музея Лувр и собора Парижской Богоматери - \nэто всего лишь некоторые из знаковых мест, которые стоит посетить.
# \nПарижские кафе, булочные и рестораны предлагают богатство французской \nкухни и возможность насладиться неповторимой
# атмосферой этого \nудивительного города.'}

# Параметра validated_data при таком подходе нет, так как не было валидации.

# Можно передать не только объект БД, но и любой объект Python с требуемой структурой(чтобы названия атрибутов
# совпадали с полями сериализатора)

# Без разницы классовые или экземплярные атрибуты, главное чтобы из можно было вызвать у объекта
class EntryClass:
    body_text = 'body_text'

    def __init__(self, headline, time):
        self.headline = headline
        self.time = time

object_entry = EntryClass('headline', 100)
serializer = EntrySerializer(object_entry)
print(serializer)
"""
EntrySerializer(<__main__.EntryClass object>):
    headline = CharField()
    body_text = CharField()
"""

print(serializer.data)  # {'headline': 'headline', 'body_text': 'body_text'}
```

3. Передача блока данных через итерируемый объект. Допустим queryset. В таком случае передаётся данный итерируемый объект
и параметр `many=True` говорящий о том, что передаётся несколько объектов.

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()

# Создаём объект сериализатора на базе queryset
serializer = EntrySerializer(Entry.objects.filter(pk__lt=4), many=True)
print(serializer)
"""
EntrySerializer(<QuerySet [<Entry: Изучение красот Мачу-Пикчу>, 
<Entry: Приключения в Амазонке>, 
<Entry: Знакомство с Парижем>]>, 
many=True):
    headline = CharField()
    body_text = CharField()
"""

print(serializer.data)  # [
# OrderedDict(
# [('headline', 'Изучение красот Мачу-Пикчу'),
# ('body_text', 'Древний город Мачу-Пикчу....')]),
# OrderedDict(
# [('headline', 'Приключения в Амазонке'),
# ('body_text', 'Амазонка - это не просто река,...')]),
# OrderedDict(
# [('headline', 'Знакомство с Парижем'),
# ('body_text', 'Париж - город любви, искусства и изысканности...')])
# ]

# При передачи данных также можно использовать параметр many, только тогда данные должны быть в каком нибудь контейнере
data = [
    {'headline': 'headline', 'body_text': 'body_text'},
    {'headline': 'headline1', 'body_text': 'body_text1'},
    {'headline': 'headline2', 'body_text': 'body_text2'},
]

serializer = EntrySerializer(data=data, many=True)
print(serializer)
"""
EntrySerializer(data=[{'headline': 'headline', 'body_text': 'body_text'}, 
{'headline': 'headline1', 'body_text': 'body_text1'}, 
{'headline': 'headline2', 'body_text': 'body_text2'}], many=True):
    headline = CharField()
    body_text = CharField()
"""
print(serializer.is_valid())  # True

print(serializer.data)  # [
# OrderedDict([('headline', 'headline'), ('body_text', 'body_text')]),
# OrderedDict([('headline', 'headline1'), ('body_text', 'body_text1')]),
# OrderedDict([('headline', 'headline2'), ('body_text', 'body_text2')])
# ]

print(serializer.validated_data) # [
# OrderedDict([('headline', 'headline'), ('body_text', 'body_text')]),
# OrderedDict([('headline', 'headline1'), ('body_text', 'body_text1')]),
# OrderedDict([('headline', 'headline2'), ('body_text', 'body_text2')])
# ]

# C объектами Python аналогично, главное, чтобы объект был итерируемым
class EntryClass:
    body_text = 'body_text'

    def __init__(self, headline, time):
        self.headline = headline
        self.time = time


object_entry = [EntryClass('headline', 100), EntryClass('headline1', 101), EntryClass('headline2', 102)]
serializer = EntrySerializer(object_entry, many=True)
print(serializer)
"""
EntrySerializer([<__main__.EntryClass object>, <__main__.EntryClass object>, <__main__.EntryClass object>], many=True):
    headline = CharField()
    body_text = CharField()
"""

print(serializer.data)  # [
# OrderedDict([('headline', 'headline'), ('body_text', 'body_text')]),
# OrderedDict([('headline', 'headline1'), ('body_text', 'body_text')]),
# OrderedDict([('headline', 'headline2'), ('body_text', 'body_text')])
# ]
```

#### 1.3 Самостоятельная(если это необходимо) сериализация в JSON и десериализация

Чтобы сериализовать в Json можно воспользоваться `JSONRenderer` или как пример стандартной библиотекой json

Пример на базе множественной сериализации объекта Python
```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()

class EntryClass:
    body_text = 'body_text'

    def __init__(self, headline, time):
        self.headline = headline
        self.time = time

object_entry = [EntryClass('headline', 100), EntryClass('headline1', 101), EntryClass('headline2', 102)]
serializer = EntrySerializer(object_entry, many=True)
print(serializer)
"""
EntrySerializer([<__main__.EntryClass object>, <__main__.EntryClass object>, <__main__.EntryClass object>], many=True):
    headline = CharField()
    body_text = CharField()
"""

print(serializer.data)  # [
# OrderedDict([('headline', 'headline'), ('body_text', 'body_text')]),
# OrderedDict([('headline', 'headline1'), ('body_text', 'body_text')]),
# OrderedDict([('headline', 'headline2'), ('body_text', 'body_text')])
# ]

from rest_framework.renderers import JSONRenderer

print(JSONRenderer().render(serializer.data))  # b'[
# {"headline":"headline","body_text":"body_text"},
# {"headline":"headline1","body_text":"body_text"},
# {"headline":"headline2","body_text":"body_text"}]'

import json

print(json.dumps(serializer.data, ensure_ascii=False).encode())  # Результат аналогичный выше

# Для десериализации из Json можно воспользоваться JSONParser или как пример стандартной библиотекой json
data_json = JSONRenderer().render(serializer.data)
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(data_json)
data = JSONParser().parse(stream)  # JSONParser читает объекты потока
print(data)  # [
# {'headline': 'headline', 'body_text': 'body_text'},
# {'headline': 'headline1', 'body_text': 'body_text'},
# {'headline': 'headline2', 'body_text': 'body_text'}
# ]

print(json.loads(data_json.decode()))  # Результат аналогичный выше
```

#### 1.4 Создание и обновление объекта на базе входных данных с использованием сериализатора

Если стоит задача создания или обновления объекта на базе входных данных, то у сериализатора необходимо переопределить
методы `create(self, validated_data)` или `update(self, instance, validated_data)` в которых необходимо описать какой объект 
возвращается в случае создания и обновления.

Рассмотрим пример на базе объекта Python. Про работу с объектом БД описано в пункте `4. Применение Serializer` и он мало
чем отличается от приведённого здесь подхода.

```python
from rest_framework import serializers
from app.models import Entry

class EntryClass:
    def __init__(self, body_text, headline, time):
        self.headline = headline
        self.body_text = body_text
        self.time = time

    def __str__(self):
        return f"{self.headline}_{self.body_text}"

class EntrySerializer(serializers.Serializer):
    headline = serializers.CharField()
    body_text = serializers.CharField()

    def create(self, validated_data):
        """
        Переопределяем для возможности создать объект на базе валидированных данных
        """
        return EntryClass(time=100, **validated_data)

    def update(self, instance, validated_data):
        """
        Переопределяем для возможности обновить объект на базе валидированных данных
        """
        instance.body_text = validated_data.get('body_text', instance.body_text)
        instance.headline = validated_data.get('headline', instance.headline)
        return instance

# Создание нового объекта
data = {
    "headline": "HEADLINE",
    "body_text": "BODY",
    "body": "b",
}
serializer = EntrySerializer(data=data)

if serializer.is_valid():
    # Создание нового объекта EntryClass
    print(serializer.save())  # HEADLINE_BODY

# Для обновления какого-то объекта обязательно необходимо передать этот объект или передать его в параметр instance

obj = EntryClass("B", "H", 100)
print(obj)  # H_B
serializer = EntrySerializer(obj, data=data)  # Или так serializer = EntrySerializer(instance=obj, data=data)
if serializer.is_valid():
    # Обновление переданного объекта obj
    print(serializer.save())  # HEADLINE_BODY
# Проверка, что объект изменил данные
print(obj)  # HEADLINE_BODY
```

### 2. Методы и атрибуты объекта сериализатора

У объектов сериализаторов есть разные методы:

* `is_valid(raise_exception=False)`: Метод, который проверяет валидность данных, переданных в сериализатор. 
Возвращает True, если данные прошли валидацию, и False в противном случае.


* `save()`: Метод, используемый для создания или обновления объекта в базе данных 
на основе десериализованных данных (serializer.validated_data). 
Обычно используется c методами `create` и `update`. Метод save() получится 
использовать при определенных методах `create` и `update`.


* `validate(attrs)`: Метод для пользовательской валидации данных в сериализаторе. 
Он предназначен для выполнения дополнительных проверок и валидации данных, которые 
не связаны с отдельными полями. Когда объект сериализатора проходит первичную 
валидацию (включая проверку типов данных, валидацию полей и т. д.), метод `validate(attrs)` 
позволяет выполнить дополнительные проверки на основе всего набора переданных 
атрибутов (attrs). В этом методе можно определить сложную логику валидации, 
которая зависит от нескольких полей или требует взаимодействия с базой данных 
или другими сервисами.

Пример дополнительной пользовательской валидации
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if len(name) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")

        if age < 18:
            raise serializers.ValidationError("Age must be at least 18.")

        return attrs
```

* `validate_empty_values(data)`: Метод, который выполняет валидацию для пустых значений полей. 
Это позволяет определить, какие поля могут быть пустыми и какие не могут.


* `get_fields()`: Метод, который возвращает словарь всех полей, объявленных в сериализаторе. 
Эти поля определяют, какие данные будут сериализованы и десериализованы.


* `bind(field_name, parent)`: Метод, который привязывает сериализатор к определенному контексту, 
такому как представление или запрос. Этот метод вызывается автоматически при создании 
объекта сериализатора.


* `get_value(dictionary)`: Метод, который получает значение для заданного атрибута из исходных 
данных, которые были переданы сериализатору.


* `fail(key)`: Метод, который вызывается, когда происходит ошибка валидации данных. 
Он используется для создания сообщений об ошибках.


* `get_attribute(instance)`: Метод, который получает атрибут из исходных данных, 
на которых производится сериализация или десериализация.


* `get_default()`: Метод, который возвращает значение по умолчанию для поля, если 
оно не было передано в исходных данных.


* `get_initial()`: Метод, который возвращает значение по умолчанию для поля, которое 
будет использоваться в исходных данных, если значение не было передано.


* `get_validators()`: Метод, который возвращает список всех валидаторов, применяемых 
к полю.


* `mani_init()`: Метод, который выполняется при инициализации сериализатора. 
Он позволяет настроить сериализатор перед его использованием.


* `run_validators(value)`: Метод, который выполняет все валидаторы для заданного поля.


* `run_validation(data)`: Метод, который выполняет все валидации для заданного поля, 
включая валидации по умолчанию, пользовательские валидации и валидации связанных полей. 
Этот метод вызывается во время процесса десериализации, когда данные из запроса 
или другого источника передаются в сериализатор для преобразования в объекты Python 
(при создании) или обновления существующих объектов (при обновлении). 
Метод `run_validation(data)` выполняет различные проверки, валидации и преобразования 
данных, чтобы убедиться, что они соответствуют ожидаемому формату и типам полей в сериализаторе.

Методы переопределяемые для создания своих сериализаторов:

* `to_representation(instance)`: Метод, который преобразует объект модели (instance) 
в словарь или другой формат данных, который будет использоваться при сериализации. 
Этот метод обычно вызывается для каждого объекта в QuerySet, когда выполняется 
сериализация списка объектов. 


* `to_internal_value(data)`: Метод, который преобразует входные данные (data), 
полученные из запроса, во внутренний формат данных, используемый в сериализаторе 
(serializer.validated_data). Этот метод обычно вызывается перед валидацией данных.

Методы переопределяемые для возможности создания и обновления элеменов в БД:

* `create(validated_data)`: Метод, который создает объект модели на основе 
валидированных данных (validated_data). Обычно используется с serializer.save() 
для создания нового объекта.


* `update(instance, validated_data)`: Метод, который обновляет существующий объект 
модели (instance) на основе валидированных данных (validated_data). Обычно используется 
с serializer.save() для обновления объекта.

У объектов сериализаторов есть разные атрибуты:

* `data`: Атрибут, который хранит сериализованные данные, готовые для отправки 
в ответе API. Эти данные представлены в виде Python-словаря (или другого подходящего 
для формата данных), соответствующего структуре вашего сериализатора. В `data` 
содержит данные, которые уже были сериализованы и готовы для отправки клиенту.


* `validated_data`: Атрибут, который хранит десериализованные и валидированные данные, 
полученные из входных данных (например, из запроса). После прохождения валидации, 
данные из входного запроса преобразуются в правильные типы Python и проходят проверку 
на соответствие заданным правилам валидации. В `validated_data` хранятся только 
данные, прошедшие валидацию.


* `initial_data`: Атрибут, который хранит необработанные данные, полученные из запроса, 
до их десериализации. Эти данные могут быть изменены в процессе валидации или десериализации.


* `errors`: Атрибут, который хранит словарь с ошибками валидации. Если данные 
не прошли валидацию, здесь будут содержаться соответствующие ошибки.


* `context`: Атрибут, который хранит контекст, переданный в сериализатор из представления. 
Этот контекст может содержать дополнительную информацию, которая может быть полезна при сериализации.


* `instance`: Атрибут, который хранит объект модели, который был создан или 
обновлен после вызова serializer.save().

И другие атрибуты

### 3. Способы валидации данных
У сериализатора есть встроенная валидация полей по типу поля, однако, если это необходимо, то можно дописать своих валидаторов

Есть несколько подходов:

#### 3.1 Валидация на уровне поля 

Вы можете задать пользовательскую валидацию на уровне полей, добавив методы 
validate_<field_name> в ваш подкласс Serializer.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value

data = {'title': 'about Django',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.validated_data)  # OrderedDict([('title', 'about Django'), ('content', '123')])

# Проверка пользовательской валидации
data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
print(serializer.validated_data)  # {}

# Пользовательская валидация применяется после стандартной валидации типов, поэтому они друг друга не перекрывают

```

Если ваше `<field_name>` объявлено в вашем сериализаторе с параметром `required=False`, то пользовательские проверки 
не будут проводиться для этого поля, если поле не включено в передаваемых данных.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value


data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
print(serializer.validated_data)  # {}

data = {'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.errors)  # {}
print(serializer.validated_data)  # OrderedDict([('content', '123')])
```

#### 3.2 Передача валидатора полю через параметр поля validators

Отдельные поля сериализатора могут включать валидаторы, 
например, путем объявления их в экземпляре поля. Добавление валидаторов идёт через параметр `validators` который принимает
список, а значит к одному полю можно последовательно применить несколько валидаторов. На параметр `required=False` реагирует
аналогично как при валидации на уровне поля.

```python
from rest_framework import serializers

def validate_title(value):
    """
    Проверка того, что заголовок содержит слово Django
    """
    if 'django' not in value.lower():
        raise serializers.ValidationError("Blog post is not about Django")
    return value

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False,
                                  validators=[validate_title])
    content = serializers.CharField()


data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
print(serializer.validated_data)  # {}

data = {'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.errors)  # {}
print(serializer.validated_data)  # OrderedDict([('content', '123')])
```

Также для полей есть возможность передать встроенный валидатор `UniqueValidator`. Этот валидатор может быть использован для обеспечения 
ограничения `unique=True` для полей модели. Находится он в `rest_framework.validators`.
Он принимает один обязательный аргумент и необязательный аргумент `messages`:

`queryset`(обязательный) - Это набор запросов, в отношении которого должна быть обеспечена уникальность.

`message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

`lookup` - Поиск, используемый для нахождения существующего экземпляра с проверяемым значением. По умолчанию 'exact'.

```python
from rest_framework import serializers, validators
from app.models import Entry, Blog, Author
from datetime import date


class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField(validators=[
        validators.UniqueValidator(queryset=Entry.objects.all())
    ])  # headline должно быть уникальным среди всех записей Entry, можно сделать допустим фильтрацию
    # и сделать уникальным для определенное время
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)


data = {
    'blog': "1",
    'headline': 'Изучение красот Мачу-Пикчу',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'headline': [ErrorDetail(string='This field must be unique.', code='unique')]}
```

#### 3.3 Валидация на уровне объекта

Чтобы выполнить любую другую проверку, требующую доступа к нескольким полям, добавьте 
метод под названием `validate()` в ваш подкласс Serializer. Этот метод принимает единственный аргумент, который 
является словарем значений полей. При необходимости он должен вызывать сигнал `serializers.ValidationError` 
или просто возвращать проверенные значения.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate(self, attrs):
        """
        Проверка того, что заголовок содержит слово Django
        """
        if 'django' not in attrs['title'].lower():
            raise serializers.ValidationError("Blog post is not about Django")
        if attrs['content'].isdigit():
            raise serializers.ValidationError("content is not digits")
        return attrs


data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')]}
print(serializer.validated_data)  # {}
```

Если необходимо вывести все ошибки или вывести конкретные ошибки по ключу поля, то можно вывести словарь с ошибками.
Также в части полей с параметрами `required=False` - то `validate()` вызывается всегда, поэтому при передаче необходимо
проверять что поле есть в атрибутах.

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    content = serializers.CharField()

    def validate(self, attrs):
        """
        Проверка того, что заголовок содержит слово Django
        """
        errors = {}

        title = attrs.get('title')
        if title and 'django' not in title.lower():
            errors['title'] = "Blog post is not about Django"
        if attrs['content'].isdigit():
            errors['content'] = "content is not digits"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs


data = {'title': 'about',
        'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'title': [ErrorDetail(string='Blog post is not about Django', code='invalid')],
# 'content': [ErrorDetail(string='content is not digits', code='invalid')]}
print(serializer.validated_data)  # {}

data = {'content': '123'}
serializer = BlogPostSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'content': [ErrorDetail(string='content is not digits', code='invalid')]}
```

#### 3.4 Передача валидаторов через class Meta

В Django Rest Framework (DRF) можно настроить валидаторы через `class Meta` 
внутри сериализатора, используя атрибут `validators`.

Атрибут `validators` в `class Meta` позволяет задать список функций-валидаторов для полей сериализатора. 
Эти валидаторы будут вызываться вместе с другими встроенными валидаторами DRF при валидации данных.

В `validators` можно передать как пользовательские, так и встроенные валидаторы. Среди встроенных валидаторов применяемым к
классам сериализатора (`class Meta`) можно передать:
  * `rest_framework.serializers.UniqueTogetherValidator` - Этот валидатор можно использовать для наложения ограничений 
unique_together на экземпляры модели. `UniqueTogetherValidator` используется для проверки уникальности комбинации 
значений нескольких полей вместе. Это полезно, когда вы хотите, чтобы комбинация значений в нескольких полях была уникальной. 
Например, вы можете использовать этот валидатор, чтобы гарантировать, что комбинация значений в полях "username" и "email" 
уникальна в вашей модели пользователей. `UniqueTogetherValidator` имеет два обязательных аргумента и один необязательный аргумент `messages`:

`queryset`(обязательный) - Это набор запросов, в отношении которого должна быть обеспечена уникальность.

`fields`(обязательный) - Список или кортеж имен полей, которые должны составлять уникальный набор. 
Они должны существовать как `поля в классе сериализатора`.

`message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

  * `rest_framework.serializers.UniqueForDateValidator`, `rest_framework.serializers.UniqueForMonthValidator`, 
`rest_framework.serializers.UniqueForYearValidator` - Эти валидаторы могут быть использованы для наложения ограничений 
`unique_for_date` , `unique_for_month` и `unique_for_year` на экземпляры модели. Они принимают следующие аргументы:

`queryset`(обязательный) - Это набор запросов, в отношении которого должна быть обеспечена уникальность.

`field`(обязательный) - Имя поля, по которому будет проверяться уникальность в заданном диапазоне дат. 
Оно должно существовать как `поле в классе сериализатора`.

`date_field`(обязательный) - Имя поля, которое будет использоваться для определения диапазона дат для ограничения уникальности. 
Оно должно существовать как `поле в классе сериализатора`.

`message` - Сообщение об ошибке, которое должно быть использовано при неудачной валидации.

```python
# Рассмотрим пример с применением нескольких различных валидаторов 
from rest_framework import serializers, validators
from app.models import Entry, Blog, Author
from datetime import date

def authors_validate(value):
    # В концепции class Meta будет передавать все доступные поля
    if len(value['authors']) < 2:
        raise serializers.ValidationError({'authors': "Число авторов должно быть более 1"})
    return value

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField(validators=[
        validators.UniqueValidator(queryset=Entry.objects.all())
    ])  # Валидация на уникальный headline для таблицы Entry
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

    class Meta:
        validators = [
            # Пользовательская валидация на число авторов
            authors_validate,
            # Валидация на совместное уникальное значение по полям number_of_comments и body_text таблицы Entry
            serializers.UniqueTogetherValidator(
                queryset=Entry.objects.all(),
                fields=['number_of_comments', 'body_text']
            ),
            # Валидация на уникальное значение поля rating при годе взятом из поля pub_date таблицы Entry
            serializers.UniqueForYearValidator(
                queryset=Entry.objects.all(),
                field='rating',
                date_field='pub_date'
            )
        ]

# Далее будет рассмотрено постепенное изменение входных данных, чтобы убрать ошибки
data = {
    'blog': "1",
    'headline': 'Изучение красот Мачу-Пикчу',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1],
    'number_of_comments': 2,
    'rating': 0.0,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'headline': [ErrorDetail(string='This field must be unique.', code='unique')]}

# Убираем ошибку неуникального headline. Допустим headline='Изучение'
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1],
    'number_of_comments': 2,
    'rating': 0.0,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'authors': [ErrorDetail(string='Число авторов должно быть более 1', code='invalid')]}

# Убираем ошибку минимального количества авторов. Допустим authors=[1,2]
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.0,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'rating': [ErrorDetail(string='This field must be unique for the "pub_date" year.', code='unique')]}

# Убираем ошибку неуникального рейтинга в году поля pub_date. Допустим rating=0.01
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.01,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'non_field_errors': [ErrorDetail(string='The fields number_of_comments, body_text must make a unique set.', code='unique')]}

# Убираем последнюю ошибку связанную с неуникальностью пары связки полей number_of_comments и body_text.
# Достаточно изменить что-то одно из полей, чтобы сделать их связку уникальной, допустим number_of_comments=3
data = {
    'blog': "1",
    'headline': 'Изучение',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 3,
    'rating': 0.01,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.errors)  # {}
```
При использовании встроенных валидаторов в Django Rest Framework, каждый валидатор будет вызываться независимо, и если 
он вызывает ошибку, процесс валидации завершится, и остальные валидаторы `не будут выполнены`. 
Это обеспечивает определенную логику работы валидаторов и предотвращает лишнюю нагрузку при нахождении первой ошибки.

На практике редко требуется условие выведения всех ошибок валидаторов за раз. Но если это необходимо, то можно решить данную задачу
определением всех валидаторов в методе `validate` сериализатора. Правда использование встроенных валидаторов таких как 
UniqueValidator, UniqueTogetherValidator, UniqueForYearValidator и т.д. может иметь достаточно специфичный вид.

```python
from rest_framework import serializers, validators
from app.models import Entry, Blog, Author
from datetime import date


def authors_validate(value):
    if len(value['authors']) < 2:
        raise serializers.ValidationError({'authors': "Число авторов должно быть более 1"})
    return value

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

    def validate(self, data):
        errors = {}
        # Проверка числа авторов
        try:
            authors_validate(data)
        except serializers.ValidationError as e:
            for field, error in e.detail.items():
                errors[field] = error

        # Проверка на уникальность headline
        unique_validator = validators.UniqueValidator(queryset=Entry.objects.all())
        try:
            unique_validator(data.get('headline'), self.fields['headline'])
        except serializers.ValidationError as e:
            errors['headline'] = e.detail

        # Вызываем валидатор UniqueTogetherValidator с переданными данными
        unique_together_validator = serializers.UniqueTogetherValidator(
            queryset=Entry.objects.all(),
            fields=['number_of_comments', 'body_text']
        )
        try:
            unique_together_validator(data, self)
        except serializers.ValidationError as e:
            errors['non_field_errors'] = e.detail

        # Проверка на уникальность по году
        unique_year_validator = serializers.UniqueForYearValidator(
                queryset=Entry.objects.all(),
                field='rating',
                date_field='pub_date'
            )
        try:
            unique_year_validator(data, self)
        except serializers.ValidationError as e:
            for field, error in e.detail.items():
                errors[field] = error

        # Если есть хотя бы одна ошибка, то выводим исключение
        if errors:
            raise serializers.ValidationError(errors)

        return data


data = {
    'blog': "1",
    'headline': 'Изучение красот Мачу-Пикчу',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1],
    'number_of_comments': 2,
    'rating': 0.0,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'authors': [ErrorDetail(string='Число авторов должно быть более 1', code='invalid')],
# 'headline': [ErrorDetail(string='This field must be unique.', code='unique')],
# 'non_field_errors': [ErrorDetail(string='The fields number_of_comments, body_text must make a unique set.', code='unique')],
# 'rating': [ErrorDetail(string='This field must be unique for the "pub_date" year.', code='unique')]}
```

### 4. Примеры использования сериализаторов

Ниже рассмотрим пару примеров создания сериализаторов разными классами на примере 
одной задачи, `создать сериализатор API, позволяющего получить все записи блогов`.

### 5. Применение общего класса Serializer

Ниже приведен пример для случая сериализации, без возможности создания или обновления
объекта БД.

```python
from rest_framework import serializers
from app.models import Blog, Author, Entry
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    # Для работы с поле много ко многому указываем many=True
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

# Можно передавать объекты БД
serializer = EntrySerializer(Entry.objects.get(pk=3))
print(serializer.data)  # {'blog': 1, 'headline': 'Знакомство с Парижем', 'body_text':
# 'Париж - город любви, искусства и изысканности. \nЗнакомство с Парижем - это погружение в его узкие улочки,
# исторические \nдостопримечательности и культурную сцену. Прогулка по набережной Сены, \nпосещение Эйфелевой башни,
# музея Лувр и собора Парижской Богоматери - \nэто всего лишь некоторые из знаковых мест, которые стоит посетить.
# \nПарижские кафе, булочные и рестораны предлагают богатство французской \nкухни и возможность насладиться неповторимой
# атмосферой этого \nудивительного города.', 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'authors': [2, 4, 6], 'number_of_comments': 7, 'number_of_pingbacks': 5, 'rating': 4.7}

"""Также можно передавать непосредственно данные, но механизм сериализатора устроен так, что если передаются данные,
то их необходимо предварительно валидировать и затем произойдут дальнейшие необходимые запросы в БД
Если данные не валидны, то атрибут validated_data будет пустым"""
data = {
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True. Без вызова is_valid не получится получить validated_data или errors
print(serializer.validated_data)  # OrderedDict([('blog', <Blog: Путешествия по миру>),
# ('headline', 'Hello World'), ('body_text', 'This is my first blog post.'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
# ('mod_date', datetime.date(2023, 7, 30)),
# ('authors', [<Author: alexander89>, <Author: ekaterina_blog>, <Author: maxim_writer>]),
# ('number_of_comments', 0), ('number_of_pingbacks', 0), ('rating', 0)])
print(serializer.data)  # {'blog': 1, 'headline': 'Hello World',
# 'body_text': 'This is my first blog post.', 'pub_date': '2023-07-19T12:00:00Z',
# 'mod_date': '2023-07-30', 'authors': [1, 2, 3], 'number_of_comments': 0,
# 'number_of_pingbacks': 0, 'rating': 0.0}

"""В data ключ 'blog' c неверной валидацией, так как ожидается ссылка на отношение к ключу строки таблицы БД. Валидация
проверяет существование ключа, поэтому ключ 0, -1, 100(так как его просто не существует записи в БД по такому ключу)
не пройдут валидацию"""
data = {
    'blog': "rr",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'blog': [ErrorDetail(string='Incorrect type. 
# Expected pk value, received str.', code='incorrect_type')]}
print(serializer.validated_data)  # {}
#  Так как валидация не прошла, то и данные с БД не были подтянуты при сериализации. Данные показывает, те, что были на входе
print(serializer.data)  # {'blog': 'rr', 'headline': 'Hello World',
# 'body_text': 'This is my first blog post.', 'pub_date': '2023-07-19T12:00:00Z',
# 'authors': [1, 2, 3]}
```

Если необходимо иметь возможность создания или обновления объекта БД(или вашей модели) после валидации, 
то необходимо переопределить методы `create(self, validated_data)` или 
`update(self, instance, validated_data)` в которых необходимо описать какой объект 
возвращается в случае создания и обновления.

#### 5.1 Создание объекта в БД

Если экземпляр сериализатора создан с использованием данных из запроса или 
другого источника (например, `serializer = MySerializer(data=request.data)`), 
и эти данные проходят валидацию (метод `is_valid()` возвращает `True`), 
то DRF выполняет создание нового объекта в базе данных с использованием метода 
`create()` сериализатора.

```python
from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

    def create(self, validated_data):
        # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
        # Необходимо будет из данных как-то удалить authors и создать объект, а затем заполнить authors
        # Или передавать каждый параметр без authors
        authors = validated_data["authors"]
        validated_data.pop("authors")  # Удаляем авторов из словаря
        instance = Entry(**validated_data)  # Создаём объект
        instance.save()  # Сохраняем в БД
        instance.authors.set(authors)  # Заполняем все в связи многое ко многому
        return instance
        """
        Если бы не было связей много ко многому, то можно было бы записать так вместо всех строк
        return Entry.objects.create(**validated_data)"""

data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)
if serializer.is_valid():
    print(repr(serializer.save()))  # <Entry: Hello World>
    """То что мы указали в данных 'id': "1" не вызовет обновление данных, 
    создастся новая строка в БД. 
    Для обновления данных есть немного другая запись"""
```

То что мы указали в данных 'blog': "1" не вызовет обновление данных, создастся 
новая строка в БД. Для обновления данных есть немного другая запись.

#### 5.2 Обновление объекта в БД

Если экземпляр сериализатора создан с существующим объектом из базы данных 
(например, `serializer = MySerializer(instance=my_instance)`), и обновляемые данные 
проходят валидацию, то DRF выполняет обновление существующего объекта в базе данных 
с использованием метода `update()` сериализатора. 

Именно наличие `instance` при инициализации сериализатора определяет что будет 
обновление, а не создание нового объекта.

Допустим объявим сразу и `create` и `update`, а решение будем принимать исходя 
из наличия `id` блога в принимаемых данных.

```python
from rest_framework import serializers
from app.models import Entry, Blog, Author
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

    def create(self, validated_data):
        # Так как есть связь многое ко многому, то создание объекта будет немного специфичное
        # Необходимо будет из данных как-то удалить authors и создать объект, а затем заполнить authors
        # Или передавать каждый параметр без authors
        authors = validated_data["authors"]
        validated_data.pop("authors")  # Удаляем авторов из словаря
        instance = Entry(**validated_data)  # Создаём объект
        instance.save()  # Сохраняем в БД
        instance.authors.set(authors)  # Заполняем все в связи многое ко многому
        return instance
        """
        Если бы не было связей много ко многому, то можно было бы записать так вместо всех строк
        return Entry.objects.create(**validated_data)"""

    def update(self, instance, validated_data):
        for tag, value in validated_data.items():
            if tag != 'authors':
                setattr(instance, tag, value)
            else:
                instance.authors.set(value)  # Так как для отношения многое ко многому немного другая запись
        """Или можно руками внести все поля где будут изменения (удобно, когда необходимо явно указать какие поля 
        изменяются вне зависимости от параметров поля)
        instance.headline = validated_data.get('headline', instance.headline)
        instance.body_text = validated_data.get('body_text', instance.body_text)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.mod_date = validated_data.get('mod_date', instance.mod_date)
        instance.number_of_comments = validated_data.get('number_of_comments', instance.number_of_comments)
        instance.number_of_pingbacks = validated_data.get('number_of_pingbacks', instance.number_of_pingbacks)
        instance.rating = validated_data.get('rating', instance.rating)"""
        instance.save()  # Сохранение изменений в БД
        return instance

data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

my_instance = Entry.objects.get(pk=data["id"])  # объявляем объект для редактирования
serializer = EntrySerializer(instance=my_instance, data=data)  # Запись для обновления строки в БД. instance передаём
# вместе с data, при сериализации id не будет участвовать (так как не определён в классовых атрибутах EntrySerializer),
# он существует в data только для более удобного создания instance.

# serializer = EntrySerializer(data=data)  # запись для создания объекта
if serializer.is_valid():
    print(repr(serializer.save()))  # <Entry: Hello World>
```

#### 5.3 Немного про `read_only=True` и `write_only=True` для связанных полей

Для связанных полей есть определенные комбинации как можно использовать поля

Если используется `read_only=True`, то `queryset` не используется. Данная конструкция не позволит изменить связанные ключи
и удобна для обновления(update()) данных БД, но при создании объекта(create()) произойдёт ошибка так как нужны ключи 
создаваемых полей. Это можно поправить в APIView, ViewSet и т.д.

```python
from rest_framework import serializers
from app.models import Entry
from datetime import date

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(read_only=True)
    headline = serializers.CharField()
    body_text = serializers.CharField()
    pub_date = serializers.DateTimeField()
    mod_date = serializers.DateField(default=date.today())
    authors = serializers.PrimaryKeyRelatedField(read_only=True,
                                                 many=True)
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

    def create(self, validated_data):
        instance = Entry(**validated_data)  # Создаём объект 
        instance.save()  # Сохраняем в БД (получим ошибку, так как в validated_data нет blog,
        # ввиду read_only=True) 
        return instance

    def update(self, instance, validated_data):
        # При обновлении нет разницы, так как поля blog и authors не обновляются
        for tag, value in validated_data.items():
            setattr(instance, tag, value)
        instance.save()  # Сохранение изменений в БД
        return instance

data = {
    'id': 1,
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

# Обновление
my_instance = Entry.objects.get(pk=data["id"])
serializer = EntrySerializer(instance=my_instance, data=data)

if serializer.is_valid():
    print(repr(serializer.save()))  # <Entry: Hello World>

# Создание
serializer = EntrySerializer(data=data)  # запись для создания объекта
if serializer.is_valid():
    print(repr(serializer.save()))  # Получаем ошибку django.db.utils.IntegrityError: NOT NULL constraint failed: app_entry.blog_id
```

`write_only=True` обязывает использовать десериализацию входных полей. Удобно когда обязательно нужно изменять значения.
Допустим 
```python
blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)
```

### 6. Применение класса ModelSerializer

`ModelSerializer` - это обычный `Serializer`, за исключением того, что:

* Набор полей по умолчанию заполняется автоматически.
* Набор валидаторов по умолчанию заполняется автоматически.
* Предусмотрены реализации по умолчанию `.create()` и `.update()`.

Процесс автоматического определения набора полей сериализатора
на основе полей модели достаточно сложно, но вы почти наверняка
не нужно копаться в реализации.

Если класс `ModelSerializer` ***не*** генерирует набор полей,
вам нужно, вы должны либо явно объявить дополнительные/отличающиеся поля на
класс сериализатора или просто используйте класс сериализатора.

`ModelSerializer` и `HyperlinkedModelSerializer` отличаются от `Serializer`, так как и них основная донастройка производится
в `class Meta`. Однако, так как они наследуются от `Serializer`, то с ними можно делать тоже самое, что и с `Serializer`

Для работы с `ModelSerializer` в `class Meta` обязательно необходимо указать обязательно 2 поля: `model` и `fields`
```python
from rest_framework import serializers
from app.models import Entry

class EntryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


serializer = EntryModelSerializer()
print(serializer)
"""EntryModelSerializer():
    id = IntegerField(label='ID', read_only=True)
    headline = CharField(max_length=255)
    body_text = CharField(style={'base_template': 'textarea.html'})
    pub_date = DateTimeField(required=False)
    mod_date = DateField(read_only=True)
    number_of_comments = IntegerField(required=False)
    number_of_pingbacks = IntegerField(required=False)
    rating = FloatField(required=False)
    blog = PrimaryKeyRelatedField(queryset=Blog.objects.all())
    authors = PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=Author.objects.all())"""

# Создание новой строки в БД
data = {
    'blog': "1",
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryModelSerializer(data=data)
print(serializer.is_valid())  # True
print(repr(serializer.save()))  # <Entry: Hello>

# Обновление строки в БД. Как и в Serializer необходимо указать объект БД который будем изменять, это будет параметр
# instance
serializer = EntryModelSerializer(instance=Entry.objects.get(pk=1), data=data)
print(serializer.is_valid())  # True
print(repr(serializer.save()))  # <Entry: Hello> Обновление строки в таблице Entry с id ключа 1, тот что передавали в instance
```

Если необходимо поменять поле или добавить валидаторов, как на примере Serializer, то это можно сделать абсолютно также
как и в Serializer.

```python
from rest_framework import serializers, validators
from app.models import Entry

def authors_validate(value):
    if len(value['authors']) < 2:
        raise serializers.ValidationError({'authors': "Число авторов должно быть более 1"})
    return value

class EntryModelSerializer(serializers.ModelSerializer):
    headline = serializers.CharField(validators=[
        validators.UniqueValidator(queryset=Entry.objects.all())
    ])

    def validate(self, attrs):
        return authors_validate(attrs)

    class Meta:
        model = Entry
        fields = '__all__'
        validators = [
            # Валидация на совместное уникальное значение по полям number_of_comments и body_text таблицы Entry
            serializers.UniqueTogetherValidator(
                queryset=Entry.objects.all(),
                fields=['number_of_comments', 'body_text']
            ),
            # Валидация на уникальное значение поля rating при годе взятом из поля pub_date таблицы Entry
            serializers.UniqueForYearValidator(
                queryset=Entry.objects.all(),
                field='rating',
                date_field='pub_date'
            )
        ]


data = {
    'blog': "1",
    'headline': 'Изучение красот Мачу-Пикчу',
    'body_text': 'Древний город Мачу-Пикчу, скрытый среди гор Анд, привлекает \nпутешественников со всего мира своей '
                 'уникальной красотой и загадочностью. \nИзучение этого археологического чуда предлагает нам уникальную '
                 'возможность \nпогрузиться в инковскую культуру и исследовать их удивительные инженерные \nдостижения. '
                 'Путешественники могут отправиться на треккинговый маршрут, \nподняться на вершину Хуайна Пикчу и '
                 'насладиться потрясающим видом на \nдревний город. Изучение Мачу-Пикчу - это не только путешествие '
                 'во времени, \nно и возможность узнать больше о древних цивилизациях и их наследии.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1],
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryModelSerializer(data=data)
print(serializer)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'rating': [ErrorDetail(string='This field must be unique for the "pub_date" year.', code='unique')]}
```

### 7. Применение класса HyperlinkedModelSerializer

Тип `ModelSerializer`, который вместо этого использует гиперссылки.
первичных ключевых отношений. 

Конкретно:
* Поле «url» включено вместо поля «id».
* Отношения с другими экземплярами представляют собой гиперссылки, а не первичные ключи.


```python
from rest_framework import serializers
from app.models import Entry


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


serializer = EntryHyperlinkedModelSerializer()
print(serializer)
"""EntryHyperlinkedModelSerializer():
    url = HyperlinkedIdentityField(view_name='entry-detail')
    headline = CharField(max_length=255)
    body_text = CharField(style={'base_template': 'textarea.html'})
    pub_date = DateTimeField(required=False)
    mod_date = DateField(read_only=True)
    number_of_comments = IntegerField(required=False)
    number_of_pingbacks = IntegerField(required=False)
    rating = FloatField(required=False)
    blog = HyperlinkedRelatedField(queryset=Blog.objects.all(), view_name='blog-detail')
    authors = HyperlinkedRelatedField(allow_empty=False, many=True, queryset=Author.objects.all(), view_name='author-detail')"""

# Создание новой строки в БД
data = {
    'blog': "1",
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryHyperlinkedModelSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'blog': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')],
# 'authors': [ErrorDetail(string='Incorrect type. Expected URL string, received int.', code='incorrect_type')]}

# В этом кроется основное отличие от ModelSerializer, так как в HyperlinkedModelSerializer для связанных полей
# передаются не id, а url по которым обрабатываются данные объекты

data = {
    'blog': 'http://example.com/blogs/1/',  # Гиперссылка на блог с id=1
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': ['http://example.com/authors/1/', 'http://example.com/authors/2/'], # Гиперссылки на авторов с id=1 и id=2
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryHyperlinkedModelSerializer(data=data)
print(serializer.is_valid())  # False
# Однако даже сейчас будет ошибка так как нет обработчика корректно отрабатывающего по приведенным ссылкам.
# Гиперссылки/URL должны указывать на конкретные представления (view) в вашем приложении,
# которые обрабатывают соответствующие запросы.
print(serializer.errors)  # {'blog': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')],
# 'authors': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')]}
```

Чтобы это поправить необходимо создать корректные обработчики view и зарегистрировать их url

Для примера можно написать простейший обработчик в приложении `app` файле `views.py`

```python
# app.views
from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Blog, Author

class BlogDetail(View):
    def get(self, request, pk):
        data = Blog.objects.filter(pk=pk).values('name', 'tagline')
        return HttpResponse(data)

class AuthorDetail(View):
    def get(self, request, pk):
        data = Author.objects.filter(pk=pk).values('name', 'email')
        return HttpResponse(data)
```
Далее зарегистрируем в `urls.py` в папке `project`. Можно идти по стандартному пути (создать urls.py в приложении app,
затем прописать там пути и уже затем зарегистрировать их в `urls.py` в папке `project`), но для экономии действий пропишу
в `urls.py` в папке `project`

```python
from django.contrib import admin
from django.urls import path, include
from app.views import BlogDetail, AuthorDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('blogs/<int:pk>/', BlogDetail.as_view(), name='blog-detail'),  # URL для представления BlogDetail
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),  # URL для представления AuthorDetail
]
```
Видно что мы используем пространство имен, допустим `name='blog-detail'` или `name='author-detail'` имена взяты из описания
сериализатора, вырезка из код выше про сериализатор 
```python
print(serializer)
"""EntryHyperlinkedModelSerializer():
    url = HyperlinkedIdentityField(view_name='entry-detail')
    headline = CharField(max_length=255)
    body_text = CharField(style={'base_template': 'textarea.html'})
    pub_date = DateTimeField(required=False)
    mod_date = DateField(read_only=True)
    number_of_comments = IntegerField(required=False)
    number_of_pingbacks = IntegerField(required=False)
    rating = FloatField(required=False)
    blog = HyperlinkedRelatedField(queryset=Blog.objects.all(), view_name='blog-detail')
    authors = HyperlinkedRelatedField(allow_empty=False, many=True, queryset=Author.objects.all(), view_name='author-detail')"""
```
У `blog` и `authors` в HyperlinkedRelatedField автоматически передаётся `view_name` именно это значение необходимо 
передать в `name` при регистрации.

Однако можно самостоятельно указать своё имя обработчика, но придётся явно указать поле. Допустим

```python
class EntryHyperlinkedModelSerializer(HyperlinkedModelSerializer):
    blog = HyperlinkedRelatedField(queryset=Blog.objects.all(), view_name='my_detail')
    class Meta:
        model = Entry
        fields = '__all__'
```
Тогда при регистрации можно в параметр `name` передать `'my_detail'`. Как пример.

```python
path('blogs/<int:pk>/', BlogDetail.as_view(), name='my_detail')
```
После регистрации обработчиков теперь тот же код у сериализатора будет нормально отрабатывать. Сохранение и обновление
аналогично ModelSerializer

```python
from rest_framework import serializers
from app.models import Entry


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


serializer = EntryHyperlinkedModelSerializer()
print(serializer)
"""EntryHyperlinkedModelSerializer():
    url = HyperlinkedIdentityField(view_name='entry-detail')
    headline = CharField(max_length=255)
    body_text = CharField(style={'base_template': 'textarea.html'})
    pub_date = DateTimeField(required=False)
    mod_date = DateField(read_only=True)
    number_of_comments = IntegerField(required=False)
    number_of_pingbacks = IntegerField(required=False)
    rating = FloatField(required=False)
    blog = HyperlinkedRelatedField(queryset=Blog.objects.all(), view_name='blog-detail')
    authors = HyperlinkedRelatedField(allow_empty=False, many=True, queryset=Author.objects.all(), view_name='author-detail')"""

# Создание новой строки в БД
data = {
    'blog': "1",
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2],
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryHyperlinkedModelSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'blog': [ErrorDetail(string='Invalid hyperlink - No URL match.', code='no_match')],
# 'authors': [ErrorDetail(string='Incorrect type. Expected URL string, received int.', code='incorrect_type')]}

# В этом кроется основное отличие от ModelSerializer, так как в HyperlinkedModelSerializer для связанных полей
# передаются не id, а url по которым обрабатываются данные объекты

data = {
    'blog': 'http://example.com/blogs/1/',  # Гиперссылка на блог с id=1
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': ['http://example.com/authors/1/', 'http://example.com/authors/2/'], # Гиперссылки на авторов с id=1 и id=2
    'number_of_comments': 2,
    'rating': 0.0,
}

# Создание объекта в БД
serializer = EntryHyperlinkedModelSerializer(data=data)
print(serializer.is_valid())  # True  Хотя при проходе через http://example.com/authors/1/ ничего не обработается,
# но обработчик получил значения из БД.
print(serializer.validated_data)  # OrderedDict([('headline', 'Hello'), ('body_text', 'World'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
# ('number_of_comments', 2), ('rating', 0.0), ('blog', <Blog: Путешествия по миру>),
# ('authors', [<Author: alexander89>, <Author: ekaterina_blog>])])
print(repr(serializer.save()))  # <Entry: Hello>

# Обновление объекта в БД
instance = Entry.objects.get(pk=1)
serializer = EntryHyperlinkedModelSerializer(instance=instance, data=data)
print(serializer.is_valid())  # True
print(repr(serializer.save()))  # <Entry: Hello>
```

По умолчанию `HyperlinkedRelatedField` не выполняет проверку домена, и позволяет использовать любой домен, 
лишь бы соответствовал ожидаемому паттерну для связанных данных. В нашем примере, ожидается паттерн 'blogs/<int:pk>/'
для поля `blog`, и 'authors/<int:pk>/' для каждого значения поля `authors`.

Это поведение допустимо, так как `HyperlinkedRelatedField` предназначен для работы с гиперссылками на связанные объекты. 
Он использует гиперссылки для представления связей между объектами вместо простых идентификаторов. 
При десериализации, `HyperlinkedRelatedField` преобразует переданные URL в соответствующие объекты на основе паттернов 
URL, и поэтому он не требует ограничения на домен.

Однако, если вы хотите добавить проверку домена и разрешить использовать только определенные домены в URL, 
вы можете провести валидацию по полю или объекту, как описывалось ранее.

Например с использованием `validate()`. Так при инициализации сразу проходит десериализация, то воспользуемся атрибутом
`initial_data` где лежат данные до десериализации.

```python
from rest_framework import serializers
from app.models import Entry


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):

    def validate(self, attrs):
        errors = {}

        if val := self.initial_data.get('blog', None):
            if not val.startswith('http://example.com'):
                errors['blog'] = 'Данный домен не обрабатывается'
        if val := self.initial_data.get('authors', None):
            if not all(map(lambda x: x.startswith('http://example.com'), val)):
                errors['authors'] = 'Данный домен не обрабатывается'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    class Meta:
        model = Entry
        fields = '__all__'

data = {
    'blog': 'http://example.com/blogs/1/',  # Гиперссылка на блог с id=1
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': ['http://example.com/authors/1/', 'http://example.com/authors/2/'], # Гиперссылки на авторов с id=1 и id=2
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryHyperlinkedModelSerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.validated_data)  # OrderedDict([('headline', 'Hello'), ('body_text', 'World'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
# ('number_of_comments', 2), ('rating', 0.0), ('blog', <Blog: Путешествия по миру>),
# ('authors', [<Author: alexander89>, <Author: ekaterina_blog>])])

data = {
    'blog': 'http://example1.com/blogs/1/',
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': ['http://example2.com/authors/1/', 'http://example3.com/authors/2/'],
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntryHyperlinkedModelSerializer(data=data)
print(serializer.is_valid())  # False
print(serializer.errors)  # {'blog': [ErrorDetail(string='Данный домен не обрабатывается', code='invalid')], 
# 'authors': [ErrorDetail(string='Данный домен не обрабатывается', code='invalid')]}
```

Если рассматривать сериализацию, то на данном этапе это проблематично, так как необходим объект request обработчика
сериализатора, об этом поговорим в представлениях и маршрутизаторах.

```python
from rest_framework import serializers
from app.models import Entry


class EntryHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

data = {
    'blog': 'http://example.com/blogs/1/',  # Гиперссылка на блог с id=1
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': ['http://example.com/authors/1/', 'http://example.com/authors/2/'],
    # Гиперссылки на авторов с id=1 и id=2
    'number_of_comments': 2,
    'rating': 0.0,
}

from django.test import RequestFactory

# Создаем экземпляр RequestFactory
factory = RequestFactory()

# Создаем фейковый GET-запрос
request = factory.get('/my-api-url/')  # Нужен путь на реальный обработчик DRF обрабатывающий данный сериализатор

serializer = EntryHyperlinkedModelSerializer(data=data, context={'request': request})
print(serializer.is_valid())  # True

# Получение данных для сериализации
print(serializer.data)
```

### 8. Настройка класса Meta у Serializer, ModelSerializer и HyperlinkedModelSerializer

В классе Meta у сериализатора можно определить различные параметры для управления его поведением. 
Вот некоторые из наиболее распространенных параметров и их описание:

* `model`: Указывает на модель, с которой связан данный сериализатор. 
Этот параметр используется в `ModelSerializer` и `HyperlinkedModelSerializer`. Используется в ModelSerializer для 
автоматического создания сериализатора на основе модели.

* `fields`: Определяет список полей, которые будут включены в сериализатор. Если нет конкретных полей, то указывается 
`fields = '__all__'`

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['headline', 'body_text', 'pub_date']

# Специально передано больше данных, чем должен обрабатывать сериализатор
data = {
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntrySerializer(data=data)
print(serializer.initial_data)  # {'headline': 'Hello', 'body_text': 'World', 'pub_date': '2023-07-19T12:00:00Z',
# 'number_of_comments': 2, 'rating': 0.0}
print(serializer.is_valid())  # True
print(serializer.data)  # {'headline': 'Hello', 'body_text': 'World', 'pub_date': '2023-07-19T12:00:00Z'}
print(serializer.validated_data)  # OrderedDict([('headline', 'Hello'), ('body_text', 'World'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')))])
```

* `exclude`: Определяет список полей, которые нужно исключить из сериализатора. 
Этот параметр применяется только в `ModelSerializer`. Параметры `fields` и `exclude` вместе не записываются.

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['blog', 'authors', 'headline', 'rating']  # Специально убрали blog и authors, так как они
        # обязательно требуются при десериализации, ввиду связи с полями через отношения.

data = {
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntrySerializer(data=data)
print(serializer.initial_data)  # {'headline': 'Hello', 'body_text': 'World', 'pub_date': '2023-07-19T12:00:00Z',
# 'number_of_comments': 2, 'rating': 0.0}
print(serializer.is_valid())  # True
print(serializer.data)  # {'body_text': 'World', 'pub_date': '2023-07-19T12:00:00Z', 'number_of_comments': 2}
print(serializer.validated_data)  # OrderedDict([('body_text', 'World'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))), ('number_of_comments', 2)])
```

* `read_only_fields`: Определяет список полей, которые должны быть только для чтения (read-only). 
Значения этих полей будут проигнорированы при десериализации. Допустим бывают ставят поля с отношениями с параметром read_only_fields.
Также помним, что можно именно поле установить с параметром `read_only=True` (см. в `fields_serializers.md`)

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['headline', 'rating']
        read_only_fields = ['blog', 'authors']  # Специально установили blog и authors, так как они
        # обязательно требуются при десериализации, ввиду связи с полями через отношения.

data = {
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'number_of_comments': 2,
    'rating': 0.0,
}

serializer = EntrySerializer(data=data)
print(serializer.initial_data)  # {'headline': 'Hello', 'body_text': 'World', 'pub_date': '2023-07-19T12:00:00Z',
# 'number_of_comments': 2, 'rating': 0.0}
print(serializer.is_valid())  # True
print(serializer.data)  # {'body_text': 'World', 'pub_date': '2023-07-19T12:00:00Z', 'number_of_comments': 2}
print(serializer.validated_data)  # OrderedDict([('body_text', 'World'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))), ('number_of_comments', 2)])
```

* `write_only_fields`: Определяет список полей, которые должны быть только для записи (write-only). 
Значения этих полей будут проигнорированы при сериализации. Допустим стандартный пример это передача пароля. Пароль 
передать можно, но показывать его нельзя.

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['headline', 'body_text', 'number_of_comments']
        read_only_fields = ['blog', 'authors']
        write_only_fields = ['rating']

# Попытаемся сериализовать объект БД
serializer = EntrySerializer(instance=Entry.objects.get(pk=3))
# Поле rating сериализуется хотя не должно
print(serializer.data)  # {'id': 3, 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'number_of_pingbacks': 5, 'rating': 4.7, 'blog': 1, 'authors': [2, 4, 6]}
```
Если через `write_only_fields` не получается добиться нужного эффекта, то всегда можно явного указать поле.

```python
from rest_framework import serializers
from app.models import Entry

class EntrySerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(required=False, write_only=True)
    class Meta:
        model = Entry
        exclude = ['headline', 'body_text', 'number_of_comments']
        read_only_fields = ['blog', 'authors']

serializer = EntrySerializer(instance=Entry.objects.get(pk=3))
# Теперь поля rating нет при сериализации
print(serializer.data)  # {'id': 3, 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'number_of_pingbacks': 5, 'blog': 1, 'authors': [2, 4, 6]}

# Аналогично при передаче данных, rating передать можно, валидировать можно, сохранить можно, но сериализовать - нет
data = {
    'headline': 'Hello',
    'body_text': 'World',
    'pub_date': '2023-07-19T12:00:00Z',
    'number_of_comments': 2,
    'rating': 0.0,
}
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True
# Данные для записи (десеарилизованные)
print(serializer.validated_data)  # OrderedDict([('rating', 0.0), ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, 
# tzinfo=zoneinfo.ZoneInfo(key='UTC')))])

# Данные для сериализации (поле rating отсутствует)
print(serializer.data)  # {'pub_date': '2023-07-19T12:00:00Z'}
```

* `validators`: Определяет список валидаторов, которые будут применены к данным сериализатора. Подробно расписано в блоке
`Способы валидации данных`

* `depth`: Управляет глубиной вложенности при сериализации связанных объектов. Он позволяет указать, на сколько уровней 
глубины следует сериализовать связанные объекты. Когда у модели есть связанные поля (например, ForeignKey, OneToOneField, 
ManyToManyField), сериализатор может автоматически включить данные связанных объектов в результат сериализации. 
Параметр `depth` позволяет контролировать, насколько "глубоко" нужно включать связанные объекты.

```python
from rest_framework import serializers
from app.models import Entry

# без параметра depth
class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['headline', 'body_text', 'number_of_comments']
        read_only_fields = ['blog', 'authors']

# Попытаемся сериализовать объект БД
serializer = EntrySerializer(instance=Entry.objects.get(pk=3))
print(serializer.data)  # {'id': 3, 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'number_of_pingbacks': 5, 'rating': 4.7, 'blog': 1, 'authors': [2, 4, 6]}

# с параметром depth=1
class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ['headline', 'body_text', 'number_of_comments']
        read_only_fields = ['blog', 'authors']
        depth = 1

# Попытаемся сериализовать объект БД
serializer = EntrySerializer(instance=Entry.objects.get(pk=3))
# Теперь blog и authors раскрыты, а не просто переданы их id
print(serializer.data)  # {'id': 3, 'pub_date': '2022-06-01T21:00:00Z', 'mod_date': '2023-07-17',
# 'number_of_pingbacks': 5, 'rating': 4.7,
# 'blog': OrderedDict([('id', 1), ('name', 'Путешествия по миру'),
# ('tagline', 'Откройте новые горизонты и погрузитесь в удивительные приключения вместе с нами!')]),
# 'authors': [OrderedDict([('id', 2), ('name', 'ekaterina_blog'), ('email', 'ekaterina.blog@yahoo.com')]),
# OrderedDict([('id', 4), ('name', 'anna_journey'), ('email', 'anna.journey@gmail.com')]),
# OrderedDict([('id', 6), ('name', 'olga_creative'), ('email', 'olga.creative@gmail.com')])]}

# Дальнейшее увеличение глубины не приведёт ни к чему, так как внутри blog и authors нет еще нераскрытых отношений

# Посмотрим как это всё сериализуется в JSON
import json
import pprint
pprint.pprint(json.dumps(serializer.data, ensure_ascii=False, indent=4))
"""
    ('{\n'
 '    "id": 3,\n'
 '    "pub_date": "2022-06-01T21:00:00Z",\n'
 '    "mod_date": "2023-07-17",\n'
 '    "number_of_pingbacks": 5,\n'
 '    "rating": 4.7,\n'
 '    "blog": {\n'
 '        "id": 1,\n'
 '        "name": "Путешествия по миру",\n'
 '        "tagline": "Откройте новые горизонты и погрузитесь в удивительные '
 'приключения вместе с нами!"\n'
 '    },\n'
 '    "authors": [\n'
 '        {\n'
 '            "id": 2,\n'
 '            "name": "ekaterina_blog",\n'
 '            "email": "ekaterina.blog@yahoo.com"\n'
 '        },\n'
 '        {\n'
 '            "id": 4,\n'
 '            "name": "anna_journey",\n'
 '            "email": "anna.journey@gmail.com"\n'
 '        },\n'
 '        {\n'
 '            "id": 6,\n'
 '            "name": "olga_creative",\n'
 '            "email": "olga.creative@gmail.com"\n'
 '        }\n'
 '    ]\n'
 '}')
"""
```
Важно помнить, что использование глубокой вложенности с `depth` может привести к проблемам с производительностью и 
увеличению размера ответа API, особенно если есть большое количество связанных объектов. Поэтому следует быть 
внимательным при использовании этого параметра и анализировать потребности своего API. В некоторых случаях, 
более эффективным решением может быть использование `serializers.Serializer` и определение кастомной логики для 
обработки связанных объектов.

#### 8.1 Устаревшие параметры
Далее будут рассмотрены устаревшие параметры(после версии 3.9.0 Django REST framework, после ноября 2018 года), 
но которые могут встретиться при исследовании кода.

* `list_serializer_class`: Этот параметр позволял определять кастомный класс сериализатора для списковых полей (например, ListField). 
Вместо этого рекомендуется определять кастомные сериализаторы и использовать их явно внутри основного сериализатора.


* `extra_kwargs`: Этот параметр использовался для определения дополнительных атрибутов и параметров для полей. Например, 
для установки валидаторов или кастомных сообщений об ошибках. Однако, начиная с DRF версии 3.1, большинство параметров, 
которые раньше определялись через `extra_kwargs`, теперь могут быть определены непосредственно внутри поля, используя 
соответствующие аргументы конструктора поля (например, validators, error_messages, required, default и т.д.). 
Таким образом, extra_kwargs более не рекомендуется для использования.


* `error_messages`: Этот параметр раньше использовался для определения кастомных сообщений об ошибках для полей. 
Вместо этого, теперь сообщения об ошибках могут быть определены непосредственно внутри поля, как атрибут error_messages.


* `model_serializer_field_mapping`: Этот параметр раньше использовался для маппинга полей модели на соответствующие 
поля сериализатора. Однако, начиная с DRF версии 3.10, этот параметр перестал использоваться, и маппинг полей модели 
определяется автоматически на основе типов полей модели.


* `serializer_related_field`: Этот параметр использовался для определения кастомных классов полей, используемых 
для сериализации связанных объектов. Вместо этого, можно использовать параметр 
serializers.ModelSerializer.serializer_related_field для определения кастомных классов полей, применяемых к связанным объектам.