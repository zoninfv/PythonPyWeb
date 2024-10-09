## Типы полей которые можно задать в сериализаторе.

В основном используется в случае использовании базового `Serializer` из `rest_framework.serializers`, но также можно 
переопределить поля для работы с `ModelSerializer` и `HyperlinkedModelSerializer`

### 1. Параметры которые можно передавать в поля
Базовый блок который будет определяться как `**params`

* `read_only=False` - Указывает, что поле доступно только для чтения (сериализации) и не будет приниматься при десериализации данных.
Такое поле используется для представления данных, которые могут быть только прочитаны клиентом, но не могут быть изменены через API.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
```

* `write_only=False` - Определяет, что поле должно быть доступно только для записи (десериализации) и не будет включено в вывод (сериализацию).
Такое поле обычно используется для чувствительных данных, которые должны быть переданы на сервер для обработки, 
но не должны быть возвращены клиенту в ответе.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
```
* `required=None` - Указывает, является ли поле обязательным при десериализации данных.
Если `required` установлен в `True`, то поле должно быть предоставлено во входных данных. Если `False`, поле может быть опущено или иметь значение `None`.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
```
* `default=empty` -  Устанавливает значение по умолчанию для поля при десериализации, если поле не было предоставлено во входных данных.
Это значение будет использовано, если при десериализации не предоставлено значение для поля.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    is_active = serializers.BooleanField(default=True)
```
* `initial=empty` - Позволяет установить значение по умолчанию для поля при создании нового объекта.
Это значение будет использовано, если при десериализации не предоставлено значение для поля.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(initial='John')
```

* `source=None` - Определяет имя атрибута модели, из которого следует получить значение для поля.
Это полезно, когда название поля в сериализаторе не совпадает с именем атрибута модели.

```python
from rest_framework import serializers

class MyModel(models.Model):
    full_name = models.CharField(max_length=100)

class MySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
```

* `label=None` - Позволяет установить человекочитаемое описание поля, которое может быть использовано при выводе данных.
Оно обычно используется для создания дружественных пользователю меток полей.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(label='Full Name')
```

* `help_text=None` - Предоставляет описание поля, которое будет использовано для предоставления помощи пользователю.
Это полезно для добавления подсказок или объяснений к полям.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(help_text='Enter your full name')
```

* `style=None` - позволяет определить стилизацию поля, такую как форматирование даты или числа.
Это используется для отображения данных в определенном стиле, например, когда нужно форматировать дату в определенном формате.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    birth_date = serializers.DateField(style={'input_type': 'date'})
```

* `error_messages=None` - Позволяет определить пользовательские сообщения об ошибках для конкретного поля.
Это полезно для переопределения стандартных сообщений об ошибках.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={'invalid': 'Invalid email format'})
```

* `validators=None` - Позволяет определить список валидаторов, которые будут применяться к полю при десериализации данных.
Валидаторы могут проверять данные на соответствие определенным критериям.

```python
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator

class MySerializer(serializers.Serializer):
    age = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
```

* `allow_null=False` -  Определяет, разрешено ли полю принимать значение None (нулевое значение) при десериализации.
Если `allow_null` установлен в `True`, то поле может быть пустым или иметь значение `None`. Если `False`, поле должно быть обязательно заполнено.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
```

#### Также в определенные поля или сериализатор можно передавать дополнительные параметры:

* `allow_empty` - указывает, разрешены ли пустые значения (например, пустые строки) для поля при десериализации.
Если `allow_empty` установлен в `True`, то пустые значения будут разрешены. Если `False`, то пустые значения будут 
считаться недопустимыми, и возникнет ошибка валидации, если такое значение будет передано при десериализации.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(allow_empty=False)
```

* `instance` - предоставляет экземпляр модели, который используется при обновлении данных через сериализатор.
Если передан instance при вызове сериализатора для десериализации, данные будут обновлены в этом экземпляре модели, 
а не создан новый.
```python
from rest_framework import serializers
from .models import MyModel

instance = MyModel.objects.get(pk=1)
serializer = MySerializer(instance=instance, data={'name': 'New Name'}, partial=True)
```

* `data` - предоставляет входные данные для десериализации через сериализатор.
Это обычно словарь или QueryDict, содержащий данные для обновления или создания экземпляра модели.

```python
from rest_framework import serializers

data = {'name': 'John', 'age': 30}
serializer = MySerializer(data=data)
```


* `partial` - указывает, что входные данные являются частичными обновлениями, и можно обновить только указанные поля.
Если partial установлен в `True`, необязательные поля могут быть пропущены, и они не будут считаться недопустимыми значениями.
```python
from rest_framework import serializers

data = {'name': 'John'}
serializer = MySerializer(data=data, partial=True)
```

* `context` - предоставляет дополнительные данные или контекст, которые могут быть использованы в процессе сериализации или десериализации.
Контекст может быть использован для передачи дополнительной информации из вида (view) или других частей приложения в сериализатор.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    def to_representation(self, instance):
        context_value = self.context.get('custom_value')
        # Дальнейшая обработка данных
```

* `max_length`, `min_length` -  позволяют задать максимальную и минимальную длину для строковых полей.
Это полезно, когда нужно ограничить допустимую длину текста.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
```

* `trim_whitespace` - Указывает, нужно ли удалять пробелы по краям входных данных перед десериализацией поля.
Если `trim_whitespace` установлен в `True`, пробелы в начале и конце строки будут удалены перед сохранением значения поля.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(trim_whitespace=True)
```
* `coerce_to_string` - Определяет, нужно ли преобразовывать значение поля в строку перед десериализацией.
Если `coerce_to_string` установлен в `True`, значение будет преобразовано в строку перед десериализацией.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    age = serializers.IntegerField(coerce_to_string=True)
```

* `localize` - Указывает, следует ли локализовать значение поля при сериализации.
Если `localize` установлен в `True`, значение будет локализовано, если поле относится к дате или числовому типу с плавающей точкой.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    birth_date = serializers.DateField(localize=True)
```

* `rounding` - Позволяет управлять округлением числовых значений при сериализации.
Может принимать значения `'up'`, `'down'`, `'half-up'`, `'half-down'`, `'half-even'`, и `'half-odd'`.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=5, decimal_places=2, rounding='half-up')
```

* `recursive` - Определяет, следует ли сериализовывать связанные модели рекурсивно или просто включать их первичные ключи.
Если recursive установлен в True, связанные модели будут сериализованы рекурсивно.

```python
from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(recursive=True)

    class Meta:
        model = Book
        fields = '__all__'
```
* `allow_folders` - Определяет, могут ли поля типа `FileField` принимать значения папок (директорий) при десериализации.
Если `allow_folders` установлен в `True`, поля `FileField` могут принимать значения папок. Если `False`, значения папок 
не будут допускаться.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    avatar = serializers.ImageField(allow_folders=True)
```

### 2. Поля сериализатора

Код для полей можно посмотреть по пути `venv\Lib\site-packages\rest_framework\fields.py`

* `BooleanField(**params)`: Поле для булевых значений (True/False).


* `CharField(allow_blank=False, trim_whitespace=True, max_length=None, min_length=None, **params)`: Строковое поле.


* `ChoiceField(choices, html_cutoff=None, 
html_cutoff_text='More than {count} items...', allow_blank=False, **params)`: Поле для выбора из предопределенных значений.


* `CreateOnlyDefault`: Используется для задания значения по умолчанию при создании объекта (POST-запрос), но не при 
обновлении (PUT-запрос) существующего объекта.
Такое поле полезно, когда вы хотите установить определенное значение для поля только при создании объекта и не хотите, 
чтобы оно перезаписывалось при обновлении объекта.
```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(default=serializers.CreateOnlyDefault(datetime.now))
```

* `CurrentUserDefault`: Используется для автоматической установки текущего пользователя (текущего запроса) в поле, 
например, поле "автор" для объекта.
Полезно, когда вы хотите автоматически устанавливать значения для определенных полей, например, поля, связанного с 
текущим пользователем.

```python
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    author = serializers.CharField(default=serializers.CurrentUserDefault())
```

* `DateField(format=empty, input_formats=None, **params)`: Поле даты.


* `DateTimeField(format=empty, input_formats=None, default_timezone=None, **params)`: Поле даты и времени.


* `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None,
                 localize=False, rounding=None, **params)`: Поле для чисел с фиксированной точностью.


* `DictField(child=rest_framework.fields._UnvalidatedField(), allow_empty=True, **params)`: Поле для словарей.


* `DurationField(max_value=None, min_value=None, **params)`: Поле для хранения длительности времени.


* `EmailField(**params)`: Поле электронной почты.


* `Field(**params)`: Базовый класс для всех полей, используется в основном для создания своих полей.


* `FileField(max_length=None, allow_empty_file=False, **params)`: Поле для загрузки файлов.


* `FilePathField(path, match=None, recursive=False, allow_files=True,
                 allow_folders=False, required=None, ChoiceField.__init__(**kwargs), **params)`: Поле для выбора файла из заданной директории.


* `FloatField(max_value=None, min_value=None, **params)`: Поле для чисел с плавающей точкой.


* `HiddenField(write_only=True, **params)`: Скрытое поле, не выводится в сериализации.


* `HStoreField(child=rest_framework.fields._UnvalidatedField(), allow_empty=True, **params)`: Поле для хранения данных в формате HStore.


* `IPAddressField(protocol='both', **params)`: Поле для IPv4 или IPv6 адресов.


* `ImageField(FileField.__init__(**kwargs))`: Поле для загрузки изображений.


* `IntegerField(max_value=None, min_value=None, **params)`: Целочисленное поле.


* `JSONField(binary=False, encoder=None, decoder=None, **params)`: Поле для хранения данных в формате JSON.


* `ListField(child=rest_framework.fields._UnvalidatedField(), allow_empty=True, max_length=None, min_length=None, **params)`: Поле для хранения списков.


* `ModelField(model_field, max_length=None, **params)`: Поле для связи с моделью. Общее поле, которое можно использовать 
для произвольного поля модели. `ModelField` используется `ModelSerializer` при работе с пользовательскими полями модели,
которые не имеют поля сериализатора для сопоставления.


* `MultipleChoiceField(allow_empty=True, **params)`: Поле для выбора из множества предопределенных значений.


* `ReadOnlyField(read_only=True, **params)`: Поле только для чтения, не используется при десериализации, просто возвращает значение поля. 
Если поле представляет собой метод без параметров, метод будет вызван и его возвращаемое значение, используемое в качестве представления.

Например, следующее вызовет `get_expiry_date()` для объекта:
```python
from rest_framework.serializers import Serializer, ReadOnlyField

class ExampleSerializer(Serializer):
        expiry_date = ReadOnlyField(source='get_expiry_date')
```

* `RegexField(regex, **params)`: Поле для данных, соответствующих заданному регулярному выражению.


* `SerializerMethodField(method_name=None, source='*', read_only=True, **params)`: Поле, использующее метод сериализатора 
для получения данных. Поле только для чтения, которое получает свое представление от вызова метода на
родительский класс сериализатора. Вызываемый метод будет иметь вид "get_{field_name}" и должен принимать один аргумент, 
который является сериализуемый объект.

Пример:
```python
from rest_framework.serializers import Serializer, SerializerMethodField

class ExampleSerializer(Serializer):
    extra_info = SerializerMethodField()

    def get_extra_info(self, obj):
        return ...  # Вычисление и возвращение
```

* `SlugField(allow_unicode=False, **params)`: Поле для URL-фрагментов (подходящие под валидацию типа slug).


* `TimeField(format=empty, input_formats=None, default_timezone=None, **params)`: Поле времени.


* `URLField(CharField.__init__(**kwargs))`: Поле URL-адреса.


* `UUIDField(format='hex_verbose', **params)`: Поле для хранения уникальных идентификаторов UUID.

### 3. Поля сериализатора, описывающее отношения с другими полями

Код для отношений полей можно посмотреть по пути `venv\Lib\site-packages\rest_framework\relations.py`

* `RelatedField(queryset=None, **params)`: Является базовым классом для полей, представляющих связанные объекты, и обычно используется для 
создания настраиваемых полей связи.
Вы можете создать свой собственный `RelatedField`, чтобы иметь полный контроль над тем, как обрабатываются связанные объекты.

```python
from rest_framework import serializers

class MyCustomRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        # Ваша логика сериализации связанного объекта
        pass

    def to_internal_value(self, data):
        # Ваша логика десериализации данных связанного объекта
        pass

class MySerializer(serializers.ModelSerializer):
    related_object = MyCustomRelatedField(queryset=RelatedModel.objects.all())

    class Meta:
        model = MyModel
        fields = ['related_object', 'name', 'age']
```

* `PrimaryKeyRelatedField()`: Используется для представления ссылки на связанный объект, используя его первичный ключ.
Это полезно, когда вы хотите работать со значениями первичных ключей вместо гиперссылок.

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
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)


data = {
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

serializer = EntrySerializer(data=data)  # Создали объект сериализатора
# Проверяем валидацию данных, обязательное условие при сериализации, нужно вызывать проверку
print(serializer.is_valid())  # True

# serializer.validated_data атрибут, который хранит десериализованные и валидированные данные, полученные из входных данных
print(serializer.validated_data)  # OrderedDict([('blog', <Blog: Путешествия по миру>),
# ('headline', 'Hello World'), ('body_text', 'This is my first blog post.'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
# ('mod_date', datetime.date(2023, 8, 8)),
# ('authors', [<Author: alexander89>, <Author: ekaterina_blog>, <Author: maxim_writer>]),
# ('number_of_comments', 0), ('number_of_pingbacks', 0), ('rating', 0)])

# serializer.data атрибут, который хранит сериализованные данные, готовые для отправки в ответе API. Эти данные представлены в виде Python-словаря
print(serializer.data)  # {'blog': 1, 'headline': 'Hello World', 'body_text': 'This is my first blog post.',
# 'pub_date': '2023-07-19T12:00:00Z', 'mod_date': '2023-08-08',
# 'authors': [1, 2, 3], 'number_of_comments': 0, 'number_of_pingbacks': 0, 'rating': 0.0}
```

Когда вы указываете `queryset=Blog.objects.all()` для поля `serializers.PrimaryKeyRelatedField`, это означает, 
что вы предоставляете полный QuerySet, который содержит все объекты модели Blog. Такая конструкция используется для того, 
чтобы позволить выбрать из всех объектов модели тот, который будет связан с текущим объектом, который сериализуется.

Поле `serializers.PrimaryKeyRelatedField` предназначено для представления отношения "многие к одному" (Many-to-One) или
"один к одному" (One-to-One) в вашем API. Оно позволяет связывать объекты одной модели с объектами другой модели, 
используя их первичные ключи.

Но если использовать параметр `many=True`, как в 
```python
authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
```
то можно работать с отношениями "многие ко многому"(Many-to-Many). В исходном коде написано, что при использовании
`many=True` возвращается объект `ManyRelatedField()` с правильной записью. Так что `PrimaryKeyRelatedField(many=True)` и
`ManyRelatedField()` равнозначны.

* `ManyRelatedField()`: Используется для сериализации или десериализации списка связанных объектов.

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
    # Поменяли предыдущую запись на ManyRelatedField
    authors = serializers.ManyRelatedField(child_relation=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all()))
    number_of_comments = serializers.IntegerField(default=0)
    number_of_pingbacks = serializers.IntegerField(default=0)
    rating = serializers.FloatField(default=0)

data = {
    'blog': "1",
    'headline': 'Hello World',
    'body_text': 'This is my first blog post.',
    'pub_date': '2023-07-19T12:00:00Z',
    'authors': [1, 2, 3],
}

# Результат далее ничем не отличается от примера ранее
serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.validated_data)  # OrderedDict([('blog', <Blog: Путешествия по миру>),
# ('headline', 'Hello World'), ('body_text', 'This is my first blog post.'),
# ('pub_date', datetime.datetime(2023, 7, 19, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC'))),
# ('mod_date', datetime.date(2023, 8, 8)),
# ('authors', [<Author: alexander89>, <Author: ekaterina_blog>, <Author: maxim_writer>]),
# ('number_of_comments', 0), ('number_of_pingbacks', 0), ('rating', 0)])
print(serializer.data)  # {'blog': 1, 'headline': 'Hello World', 'body_text': 'This is my first blog post.',
# 'pub_date': '2023-07-19T12:00:00Z', 'mod_date': '2023-08-08',
# 'authors': [1, 2, 3], 'number_of_comments': 0, 'number_of_pingbacks': 0, 'rating': 0.0}
```

* `SlugRelatedField()`: Используется для связи объекта по его slug-значению. Поле для чтения и записи, которое представляет 
цель отношения по уникальному атрибуту 'slug'.
Полезно, когда вы хотите связать объекты по их slug-значению вместо первичных ключей. Параметр `slug_field` связывает
входные данные с нужным полем.

```python
from rest_framework import serializers
from app.models import Blog, Author

class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())
    # Связали автора по его email
    author = serializers.SlugRelatedField(slug_field='email', queryset=Author.objects.all())


data = {
    'blog': "1",
    'author': 'alexander89@gmail.com',
}

serializer = EntrySerializer(data=data)
print(serializer.is_valid())  # True
print(serializer.validated_data)  # OrderedDict([('blog', <Blog: Путешествия по миру>),
# ('author', <Author: alexander89>)])
print(serializer.data)  # {'blog': 1, 'author': 'alexander89@gmail.com'}
```

* `StringRelatedField()`: Используется для представления связанных объектов в виде их строкового представления (str()).
Поле только для чтения, которое представляет свои цели, используя их простое строковое представление.
Это полезно, когда вы хотите, чтобы связанные объекты отображались в виде простых строк, а не сериализовались в сложные объекты.

Исходный код `StringRelatedField`
![img_2.png](img_2.png)

```python
from rest_framework import serializers
from app.models import Entry, Blog

# поле blog через PrimaryKeyRelatedField
class EntrySerializer(serializers.Serializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

serializer = EntrySerializer(Entry.objects.get(id=4))
print(serializer.data)  # {'blog': 1}

# поле blog через StringRelatedField
class EntrySerializer(serializers.Serializer):
    blog = serializers.StringRelatedField()

serializer = EntrySerializer(Entry.objects.get(id=4))
print(serializer.data)  # {'blog': 'Путешествия по миру'}
```
Поле blog с `StringRelatedField` изменилось так как в модели `Blog` при вызове `__str__` возвращается `self.name`

![img_3.png](img_3.png)

#### Поля с гиперссылками

Поля с гиперссылками имеют специфичное представление и их сложно отделить от общего представления. Частично рассмотрены
в `serializers.md` при рассмотрении `HyperlinkedModelSerializers`

* `HyperlinkedRelatedField`: Используется для представления ссылки на связанный объект, используя его URL (гиперссылку).
Полезно, когда вы хотите, чтобы сериализатор возвращал ссылку на связанный объект вместо его простого представления.

```python
from rest_framework import serializers
from myapp.models import RelatedModel, MyModel

class MySerializer(serializers.ModelSerializer):
    related_object = serializers.HyperlinkedRelatedField(
        view_name='related-detail',
        queryset=RelatedModel.objects.all()
    )

    class Meta:
        model = MyModel
        fields = ['related_object', 'name', 'age']
```

* `HyperlinkedIdentityField()`: Используется для представления ссылки на URL идентификатора объекта 
(обычно для detail представления объекта) вместо его простого значения.
Это полезно, когда вы хотите, чтобы сериализатор возвращал ссылку на детали объекта, а не просто его идентификатор.

```python
from rest_framework import serializers

class MySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='my-detail')

    class Meta:
        model = MyModel
        fields = ['url', 'name', 'age']
```
