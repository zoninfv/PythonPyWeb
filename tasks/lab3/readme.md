# 1. Работа с API, через view

Перед тем как работать с `Django Rest Framework` сначала посмотрим как бы можно было сделать
решение задачи доступа к ресурсам через методы `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, без него.

В приложении `db_train_alternative` во `views.py` пропишем пару отображений для работы с данными.

Создадим возможность работы с БД (отображения, изменения) таблиц приложения `db_train_alternative`

Поработаем над таблицей Author, там всего 2 поля `name` и `email` особых сложностей не должно быть.

## 1.1 GET запрос

Во `views.py` приложения `db_train_alternative` создадим отображение `AuthorREST` возвращающее json,
пропишем пока только GET запрос. Поработаем над базовым классом `View`, чтобы всё прописать руками.

Скопируйте во `views.py` и проанализируйте данный код. Здесь мы по приципу REST сформировали get запрос, т.е.
есть возможность как получить все данные из БД, так как и какие-то конкретные. После получения данных мы определяем какие
данные (поля таблицы) будут возвращаться. Если не нашли конкретного автора, то возвращаем JSON с кодом 404 и поясняющим сообщением.

```python
from django.http import JsonResponse
from django.views import View
from .models import Author
from django.views.decorators.csrf import csrf_exempt
import json


class AuthorREST(View):
    def get(self, request, id=None):

        if id is None:  # Проверяем, что требуется вернуть всех пользователей
            data = []
            for author in Author.objects.all():
                # Производим сериализацию, т.е. определяем, что именно запишется в данные для преобразования в JSON
                data_author = {'id': author.id,
                               'name': author.name,
                               'email': author.email}
                data.append(data_author)
        else:
            author = Author.objects.filter(id=id)
            if author:  # Если автор такой есть, т.е. QuerySet не пустой
                author = author.first()  # Получаем первого автора из QuerySet, так как он там один
                # Производим сериализацию, т.е. определяем, что именно запишется в данные для преобразования в JSON
                data = {'id': author.id,
                        'name': author.name,
                        'email': author.email}
            else:  # Иначе, так как автор не найден (QuerySet пустой), то возвращаем ошибку, с произвольным текстом,
                # для понимания почему произошла ошибка
                return JsonResponse({'error': f'Автора с id={id} не найдено!'},
                                    status=404,
                                    json_dumps_params={"ensure_ascii": False,
                                                       "indent": 4}
                                    )

        # После того как данные для ответа созданы - возвращаем Json объект с данными
        return JsonResponse(data, safe=False, json_dumps_params={"ensure_ascii": False,
                                                                 "indent": 4})
```

Создайте файл `urls.py` в данном приложении и опишите там пути. Опять же архитектурный стиль REST, одно отображение, но благодаря
разным методам получаются разные действия.

```python
from django.urls import path
from .views import AuthorREST


urlpatterns = [
    path('author/', AuthorREST.as_view()),
    path('author/<int:id>/', AuthorREST.as_view()),
]
```
Затем добавляем ссылку на приложение в `urls.py` в папке `project`

```python
urlpatterns = [
    # ...
    path('api_alter/', include('apps.db_train_alternative.urls')),
]
```

Проверьте работоспособность данного отображения по путям

---
Чтобы вывести всех авторов

http://127.0.0.1:8000/api_alter/author/

---
Чтобы вывести автора с id=10

http://127.0.0.1:8000/api_alter/author/10/

---
Чтобы вывести несуществующего автора

http://127.0.0.1:8000/api_alter/author/0/

---

Формально вот мы и создали свой API endpoint (точку присоединения), чтобы получать нужную нам информацию при GET запросе по адресу
`http://127.0.0.1:8000/api_alter/author/`

Туже информацию мы можем получить через `requests` в python или через `curl`.

Напомним как это делается.

### 1.1.1 requests

Для работы с `requests` воспользуемся `Python Console`, где пропишем

```python
import requests
response = requests.get('http://127.0.0.1:8000/api_alter/author/')
response.status_code
response.json()
```

![img.png](pic/img.png)

### 1.1.2 curl

Теперь в терминале (`Terminal`) обратимся к тому же адресу, но через `curl`

```text
curl http://127.0.0.1:8000/api_alter/author/
```

![img_1.png](pic/img_1.png)

### 1.1.3 postman

Также можно использовать специальные программы на примере Postman, которые позволяют проводить проверку работоспособности
API и её endpoints. 

Скачайте и установите программу [Postman](https://www.postman.com/downloads/) (если вы находитесь в классе ВИШ, то спросите у преподавателя,
где находится файл установки на компьютере). Нужна именно версия на компьютере, а не web версия, так как web версия не позволяет
обрабатывать запросы на localhost.

Зарегистрируйтесь или нажмите на использование легковесного клиента(при использовании легковесного клиента ваши запросы не сохранятся
на сервере Postman, что может быть не так удобно при использовании программы на другом компьютере)

![img_2.png](pic/img_2.png)

Создадим коллекцию, это своего рода папка с запросами на одну тему

![img_3.png](pic/img_3.png)

Назовем нашу коллекцию, допустим `Тестирование db_alternative`

Теперь добавим запросов в нашу коллекцию

![img_4.png](pic/img_4.png)

Назовем наш запрос, допустим `Get Authors` так как планируем создать GET запрос к таблице Author

![img_5.png](pic/img_5.png)

И в форме прописываем адрес для запроса и нажимаем `Send`

```text
http://127.0.0.1:8000/api_alter/author/
```

В форме ниже получаем результат. Можно сохранить данный запрос, чтобы не нужно было его заново вводить

![img_6.png](pic/img_6.png)

Postman позволяет удобно работать с группами запросов и удобно тестировать их.

## 1.2 POST запрос

Настало время передать информацию и создать нового автора в REST стиле, для этого в `AuthorREST` добавим метод `post`

```python
class AuthorREST(View):
    def get(self, request):
        # код что был
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            author = Author.objects.create(name=data['name'], email=data['email'])
            response_data = {
                'message': f'Автор успешно создан',
                'id': author.id,
                'name': author.name,
                'email': author.email
            }
            return JsonResponse(response_data, status=201,
                            json_dumps_params={"ensure_ascii": False,
                                              "indent": 4}
                            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                  "indent": 4}
                                )
```

Новую маршрутизацию проводить не нужно, так как о добавлении данных Django понимает из метода запроса POST, мы же о 
REST принципе говорим.

Теперь проверим как работает новый метод `post`

Вручную через адресную строку не проверить `post` запрос, поэтому посмотрим так как умеем

### 1.2.1 requests

Сначала с библиотекой `requests` в `PythonConsole`

```python
import requests
import json
data = {'name': 'user123', 'email': 'user123'}
url = 'http://127.0.0.1:8000/api_alter/author/'
response = requests.post(url=url, data=json.dumps(data))
response.status_code
```

![img_7.png](pic/img_7.png)

Получили ошибку 403, связанную с тем, что Django любые небезопасные запросы (те, что что-то меняют, допустим POST, PUT, DELETE)
не пропускает без csrf токена, для упрощения разработки это временно можно отключить, используя декоратор `@csrf_exempt` над методом `dispatch`
мы отключим обязательное требование этого механизма.

```python
class AuthorREST(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        # код что был
    
    def post(self, request):
        # код что был
```

Метод `dispatch` в Django-представлениях обрабатывает запросы, направляя их к соответствующим методам обработки (например, GET, POST, PUT, DELETE). 
Он является частью механизма маршрутизации и обработки запросов в Django.

По умолчанию `dispatch` определяет, какой метод (GET, POST, PUT, DELETE и т. д.) использовать для обработки входящего запроса. 
Он делает это на основе HTTP-метода, используемого в запросе. Например, если приходит запрос типа GET, то `dispatch` вызывает метод `get`. 
Если приходит запрос типа POST, то он вызывает метод `post`, и так далее.

В примере выше `csrf_exempt` используется для временного отключения защиты CSRF (Cross-Site Request Forgery) для данного представления. 
Это делается потому, что мы принимаем данные без проверки CSRF в методах post, put и delete. 
В реальном приложении необходимо активировать CSRF-защиту, но для этого примера она временно отключена для упрощения.

```python
import requests
import json
data = {'name': 'user123', 'email': 'user123'}
url = 'http://127.0.0.1:8000/api_alter/author/'
response = requests.post(url=url, data=json.dumps(data))
response.status_code
response.json()
```

![img_8.png](pic/img_8.png)

Теперь всё успешно создано, даже в БД есть запись, но вот странно, пользователь создался, но email даже не валидировался,
так как в БД теперь пользователь с email `user123`. Это связано с тем, что Django ORM по умолчанию для ускорения записи в БД
не проводит валидацию и оставляет право за разработчиком проверить поля модели самостоятельно, если это необходимо, чтобы вызвать проверку
полей (валидация) необходимо перед сохранением объекта вызвать `clean_fields()`

Удалите через админ панель созданного автора в таблице `Авторы` приложения `Db_Train_Alternative`

Затем заменить код в методе `post` на следующий (обратите внимание создание через `create` было заменено на 2 строки
объявление объекта author и вызов проверок, так как `create` не имеет `clean_fields()`):

```python
def post(self, request):
    try:
        data = json.loads(request.body)
        
        author = Author(name=data['name'], email=data['email'])
        author.clean_fields()  # Запуск валидаций
        author.save()  # Сохранение в БД
        
        response_data = {
            'message': f'Автор успешно создан',
            'id': author.id,
            'name': author.name,
            'email': author.email
        }
        return JsonResponse(response_data, status=201,
                            json_dumps_params={"ensure_ascii": False,
                                              "indent": 4}
                            )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400,
                            json_dumps_params={"ensure_ascii": False,
                                              "indent": 4}
                            )
```

А теперь повторяем код в `PythonConsole`

```python
import requests
import json
data = {'name': 'user123', 'email': 'user123'}
url = 'http://127.0.0.1:8000/api_alter/author/'
response = requests.post(url=url, data=json.dumps(data))
response.status_code
response.json()
```

И видим то, что хотели бы увидеть, ошибку, что email не валиден

![img_9.png](pic/img_9.png)

### 1.2.2 curl

Теперь в терминале (`Terminal`) обратимся к тому же адресу, но через `curl`

```text
curl -X POST http://127.0.0.1:8000/api_alter/author/ -H "Content-Type: application/json" -d "{\"name\": \"user123\", \"email\": \"user123@user.com\"}"
```

В этой команде использовано экранирование обратными слэшами (\) для обеспечения правильного формата JSON

![img_10.png](pic/img_10.png)

### 1.2.3 postman

Нажимаем на + и создаём новый запрос

![img_11.png](pic/img_11.png)

Вводим адрес

```text
http://127.0.0.1:8000/api_alter/author/
```

выбираем POST

![img_12.png](pic/img_12.png)

Далее необходимо прописать в заголовке, что мы отправляем JSON, для этого в `Headers` пропишем

| Key          | Value            |
|--------------|------------------|
| Content-Type | application/json |

![img_13.png](pic/img_13.png)

Далее переходим в `Body` выбираем `raw` (обратите внимание, чтобы сбоку стояло JSON) и прописываем там данные для отправки

```text
{
    "name": "user1",
    "email": "user1@user.com"
}
```

Затем нажимаем `Send`

![img_14.png](pic/img_14.png)

И получаем ответ

![img_15.png](pic/img_15.png)

Осталось только сохранить данный запрос, для этого нажимаем на Save

![img_16.png](pic/img_16.png)
 
В поле `Request Name` прописываем название запроса `Post Author` и сохраняем на Save

![img_17.png](pic/img_17.png)

## 1.3 PUT запрос

Далее пропишем возможность изменять данные об авторе при помощи `put` метода

```python
class AuthorREST(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        # ...

    def get(self, request, id=None):
        # ...
       
    def post(self, request):
        # ...

    def put(self, request, id):
        try:
            author = Author.objects.get(id=id)
            data = json.loads(request.body)
            # Обновляем поля
            author.name = data['name']
            author.email = data['email']
            author.clean_fields()  # Запуск валидаций
            author.save()  # Сохранение в БД
            
            response_data = {
                'message': f'Данные автора успешно изменены',
                'id': author.id,
                'name': author.name,
                'email': author.email
            }
            return JsonResponse(response_data,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
        except Author.DoesNotExist:  # Если получили ошибку
            return JsonResponse({'error': 'Автор не найден'},
                                status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
        except Exception as e:  # При любой другой ошибке
            return JsonResponse({'error': str(e)},
                                status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
```

## 1.3.1 requests

Проверим, что при изменении email пользователя на невалидный - произойдет ошибка

В `PythonConsole` пропишем

```python
import requests
import json
data = {'name': 'user123', 'email': 'user123'}
url = 'http://127.0.0.1:8000/api_alter/author/22/'
response = requests.put(url=url, data=json.dumps(data))
response.status_code
response.json()
```

![img_18.png](pic/img_18.png)

А если прописать нормально, то все поменяется

```python
import requests
import json
data = {'name': 'user12', 'email': 'user12@user.com'}
url = 'http://127.0.0.1:8000/api_alter/author/22/'
response = requests.put(url=url, data=json.dumps(data))
response.status_code
response.json()
```

![img_19.png](pic/img_19.png)

## 1.3.2 curl

С curl аналогично

Теперь в терминале (`Terminal`) обратимся к тому же адресу, но через `curl`

```text
curl -X PUT http://127.0.0.1:8000/api_alter/author/22/ -H "Content-Type: application/json" -d "{\"name\": \"user123\", \"email\": \"user123@user.com\"}"
```

![img_20.png](pic/img_20.png)

## 1.3.3 postman

Для Postman теперь пропишем запросы для PUT, сделаем их несколько, для проверки как изменения, так и появления ошибок

Для этого создаём новый запрос нажав на `+`

---

По аналогии с POST делаем с PUT

Вводим адрес

```text
http://127.0.0.1:8000/api_alter/author/22/
```

выбираем PUT

![img_21.png](pic/img_21.png)

Далее необходимо прописать в заголовке, что мы отправляем JSON, для этого в `Headers` пропишем

| Key          | Value            |
|--------------|------------------|
| Content-Type | application/json |

Далее переходим в `Body` выбираем `raw` (обратите внимание, чтобы сбоку стояло JSON) и прописываем там данные для отправки

```text
{
    "name": "user1",
    "email": "user2@user.com"
}
```

Затем нажимаем `Send`

![img_22.png](pic/img_22.png)

---

Сохраним данный запрос нажав на Save, напишем имя `Put Author Correct` и создадим отдельную папку `PUT`, чтобы сложить туда запросы PUT

![img_23.png](pic/img_23.png)

И сохраняем в данной папке

После сохранения появится следующая структура

![img_24.png](pic/img_24.png)

Теперь создадим ещё 2 PUT запроса, но с проверкой ошибок:

---
Проверка ошибки получения автора

Запрос на адрес  `http://127.0.0.1:8000/api_alter/author/0/`

В запрос не забудьте про заголовок в `Headers`

| Key          | Value            |
|--------------|------------------|
| Content-Type | application/json |

В `Body` в `raw` пропишите

```text
{
    "name": "user1",
    "email": "user2@user.com"
}
```

Выполните запрос

![img_25.png](pic/img_25.png)

Сохраните запрос в папку PUT под названием `Put Author Incorrect`

---
Проверка получения ошибки валидации email

Запрос на адрес `http://127.0.0.1:8000/api_alter/author/22/`

В запрос не забудьте про заголовок в `Headers`

| Key          | Value            |
|--------------|------------------|
| Content-Type | application/json |

В `Body` в `raw` пропишите

```text
{
    "name": "user1",
    "email": "user2"
}
```

Выполните запрос

![img_26.png](pic/img_26.png)

Сохраните запрос в папку PUT под названием `Put Author Incorrect Email`

---

Теперь структура будет выглядеть так

![img_27.png](pic/img_27.png)


## 1.4 PATCH запрос

Для частичного обновления данных используют метод `patch`

```python
class AuthorREST(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        # ...

    def get(self, request, id=None):
        # ...
       
    def post(self, request):
        # ...

    def put(self, request, id):
        # ...
    
    def patch(self, request, id):
        try:
            author = Author.objects.get(id=id)  # Получаем объект
            data = json.loads(request.body)
    
            for key, value in data.items():  # Пробегаем по данным
                setattr(author, key, value)  # Устанавливаем соответствующие значения в поля
            author.clean_fields()  # Запуск валидаций
            author.save()  # Сохранение в БД
    
            response_data = {
                'id': author.id,
                'name': author.name,
                'email': author.email
            }
            return JsonResponse(response_data,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
        except Author.DoesNotExist:
            return JsonResponse({'error': f'Автор с id={author.id} не найден'},
                                status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)},
                                status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
    
```

## 1.4.1 requests

В `PythonConsole` пропишем

```python
import requests
import json
data = {'name': 'superuser'}
url = 'http://127.0.0.1:8000/api_alter/author/22/'
response = requests.patch(url=url, data=json.dumps(data))
response.status_code
response.json()
```

![img_28.png](pic/img_28.png)

## 1.4.2 curl

Теперь в терминале (`Terminal`) обратимся к тому же адресу, но через `curl`

```text
curl -X PATCH http://127.0.0.1:8000/api_alter/author/22/ -H "Content-Type: application/json" -d "{\"name\": \"user123\"}"
```

![img_29.png](pic/img_29.png)

## 1.4.3 postman

Метод `PATCH`

Запрос на адрес `http://127.0.0.1:8000/api_alter/author/22/`

В запрос не забудьте про заголовок в `Headers`

| Key          | Value            |
|--------------|------------------|
| Content-Type | application/json |

В `Body` в `raw` пропишите

```text
{
    "email": "user2000@user.com"
}
```

Выполните запрос

![img_30.png](pic/img_30.png)

Сохраните запрос

## 1.5 DELETE запрос

Для удаления данных используют метод `delete`


```python
class AuthorREST(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        # ...

    def get(self, request, id=None):
        # ...
       
    def post(self, request):
        # ...

    def put(self, request, id):
        # ...
    
    def patch(self, request, id):
        # ...

    def delete(self, request, id):
        try:
            author = Author.objects.get(id=id)
            author.delete()
            return JsonResponse({'message': 'Автор успешно удалён'},
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
        except Author.DoesNotExist:
            return JsonResponse({'error': 'Автор не найден'},
                                status=404,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
        except Exception as e:
            return JsonResponse({'error': str(e)},
                                status=400,
                                json_dumps_params={"ensure_ascii": False,
                                                   "indent": 4},
                                )
```


## 1.5.1 requests

В `PythonConsole` пропишем

```python
import requests
url = 'http://127.0.0.1:8000/api_alter/author/23/'
response = requests.delete(url=url)
response.status_code
response.json()
```

![img_31.png](pic/img_31.png)

## 1.5.2 curl

Теперь в терминале (`Terminal`) обратимся к тому же адресу, но через `curl`

```text
curl -X DELETE http://127.0.0.1:8000/api_alter/author/22/
```

![img_32.png](pic/img_32.png)

## 1.5.3 postman

Метод `DELETE`

Запрос на неверный(такого автора нет, был удален ранее) адрес `http://127.0.0.1:8000/api_alter/author/22/`

Выполните запрос

![img_33.png](pic/img_33.png)

Сохраните запрос

## 1.6 Типовые возвращаемые статус коды и что они значат (материал для чтения)

В RESTful API обычно используются стандартные HTTP-статусы для индикации успешного или неудачного выполнения операции. 

Вот общепринятые статусы для каждого метода запроса:

### 1.6.1 GET

* Успешный запрос (Successful Request):
  * `200 OK`: Возвращается в случае успешного запроса, когда ресурс найден и возвращается в теле ответа.
* Неудача запроса (Unsuccessful Request):
  * `404 Not Found`: Возвращается, если запрашиваемый ресурс не найден.
  * `400 Bad Request`: Возвращается, если запрос содержит неверный синтаксис или некорректные параметры.

### 1.6.2 POST

* Успешное создание (Successful Creation):
  * `201 Created`: Возвращается в случае успешного создания ресурса. Новый ресурс обычно создается и его URL возвращается в заголовке ответа Location.
* Неудачное создание (Unsuccessful Creation):
  * `400 Bad Request`: Возвращается, если запрос содержит неверный синтаксис или некорректные данные.
  * `409 Conflict`: Возвращается, если создание ресурса не удалось из-за конфликта (например, дублирование уникального ключа).

### 1.6.3 PUT

* Успешное обновление (Successful Update):
  * `200 OK`: Возвращается в случае успешного обновления ресурса.
* Неудачное обновление (Unsuccessful Update):
  * `400 Bad Request`: Возвращается, если запрос содержит неверный синтаксис или некорректные данные.
  * `404 Not Found`: Возвращается, если запрашиваемый ресурс не найден.

### 1.6.4 PATCH

* Успешное обновление (Successful Update):
  * `200 OK`: Возвращается в случае, когда обновление выполнено успешно и в ответе возвращается обновленный ресурс.
  * `204 No Content`: Возвращается, когда обновление выполнено успешно, но в ответе нет тела (пустое тело).
* Неудача обновления (Unsuccessful Update):
  * `400 Bad Request`: Возвращается, если запрос содержит неверный синтаксис или некорректные данные, которые не позволяют выполнить обновление.
  * `404 Not Found`: Возвращается, если запрашиваемый ресурс не найден и не может быть обновлен.
  * `409 Conflict`: Возвращается, если возникает конфликт при попытке обновления ресурса (например, конфликт версий или данные уже устарели).

### 1.6.5 DELETE

* Успешное удаление (Successful Deletion):
  * `200 OK`: Возвращается в случае успешного удаления ресурса.
* Неудачное удаление (Unsuccessful Deletion):
  * `404 Not Found`: Возвращается, если запрашиваемый ресурс не найден.


### 1.7 Самостоятельно (для желающих)

Самостоятельно определите таблицу в БД (из тех, что имеете), с которой будете работать и опишите часть методов вашего представления под REST принцип.
Настоятельно рекомендуется пока не брать Таблицы, где есть поля с файлами и картинками, так как загрузка файлов на сервер 
в API делается немного по-другому. Будет рассмотрено в дополнительных заданиях.

Протестируйте работоспособность вашего представления через Postman


# 2. Работа с API через Django REST Framework

С пункта 1.1 до 1.5 было формирование представление возвращающее JSON, а пути обработки и методы были сделаны так, чтобы соответствовать
REST принципу. Вы видели насколько много необходимо прописать кода, чтобы сделать какие-то простейшие действия над данными в БД.

Чтобы облегчить жизнь в части создания точек подключения (endpoint) используется `Django REST Framework`.

---

В разработке

---

# Практика окончена

---

# <u>Необязательный блок</u> (выполнение по желанию, на результат следующих практик влиять не будет)

