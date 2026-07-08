# Решение задачи: Тестирование Django-приложения

## Описание выполненной работы

В данном проекте были написаны комплексные тесты для API курсов и студентов с использованием Django REST Framework и pytest.

## Фикстуры

В файле `tests/conftest.py` созданы следующие фикстуры:

- **`api_client`** — фикстура для создания экземпляра `APIClient` из DRF для выполнения HTTP-запросов.
- **`course_factory`** — фабрика для создания экземпляров модели `Course` с помощью `model_bakery`.
- **`student_factory`** — фабрика для создания экземпляров модели `Student` с помощью `model_bakery`.

## Тест-кейсы

Все тесты находятся в файле `tests/students/test_courses_api.py` и включают:

1. **`test_retrieve_course`** — проверка получения одного курса (retrieve-логика)
   - Создает курс через фабрику
   - Выполняет GET-запрос через тестовый клиент
   - Проверяет статус 200 и корректность данных

2. **`test_list_courses`** — проверка получения списка курсов (list-логика)
   - Создает два курса через фабрику
   - Выполняет GET-запрос к списку курсов
   - Проверяет статус 200 и количество возвращенных элементов

3. **`test_filter_courses_by_id`** — проверка фильтрации списка курсов по `id`
   - Создает два курса
   - Выполняет запрос с фильтром по ID одного курса
   - Проверяет, что возвращен только один курс

4. **`test_filter_courses_by_name`** — проверка фильтрации списка курсов по `name`
   - Создает два курса с разными именами
   - Выполняет запрос с фильтром по имени
   - Проверяет фильтрацию по названию

5. **`test_create_course`** — тест успешного создания курса
   - Подготавливает JSON-данные без студентов
   - Выполняет POST-запрос
   - Проверяет статус 201 и корректность созданных данных

6. **`test_update_course`** — тест успешного обновления курса
   - Создает курс через фабрику
   - Выполняет PUT-запрос с новыми данными
   - Проверяет статус 200 и обновление в БД

7. **`test_delete_course`** — тест успешного удаления курса
   - Создает курс через фабрику
   - Выполняет DELETE-запрос
   - Проверяет статус 204 и отсутствие записи в БД

8. **`test_course_max_students_limit`** — тест ограничения числа студентов на курсе
   - Параметризованный тест с двумя сценариями:
     - 20 студентов (допустимо) → статус 201
     - 21 студент (превышение лимита) → статус 400 с ошибкой валидации
   - Использует `settings` fixture для переопределения `MAX_STUDENTS_PER_COURSE`

## Технические детали

- Все тесты помечены декоратором `@pytest.mark.django_db` для использования базы данных
- Используется `model_bakery` для генерации тестовых данных
- Валидация ограничения числа студентов реализована в `CourseSerializer.validate_students()`
- Проверка максимального числа студентов использует параметр `MAX_STUDENTS_PER_COURSE` из настроек Django

## Примеры вывода pytest

### Успешный запуск (все тесты проходят)

```
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
rootdir: d:\virtual\dj-homeworks\3.4-django-testing\django_testing
configfile: pytest.ini
plugins: anyio-4.13.0, asyncio-1.4.0, django-4.12.0
asyncio: mode=Mode.STRICT, debug=False

collecting ... collected 9 items

tests/students/test_courses_api.py::test_retrieve_course PASSED          [ 11%]
tests/students/test_courses_api.py::test_list_courses PASSED             [ 22%]
tests/students/test_courses_api.py::test_filter_courses_by_id PASSED     [ 33%]
tests/students/test_courses_api.py::test_filter_courses_by_name PASSED   [ 44%]
tests/students/test_courses_api.py::test_create_course PASSED            [ 55%]
tests/students/test_courses_api.py::test_update_course PASSED            [ 66%]
tests/students/test_courses_api.py::test_delete_course PASSED            [ 77%]
tests/students/test_courses_api.py::test_course_max_students_limit[20-False] PASSED [ 88%]
tests/students/test_courses_api.py::test_course_max_students_limit[21-True] PASSED [100%]

============================== 9 passed in 0.61s ==============================
```

### Сценарий 1: Ошибка валидации (превышение лимита студентов)

При попытке создать курс с 21 студентом:

```
============================= test session starts =============================
...
tests/students/test_courses_api.py::test_course_max_students_limit[20-False] PASSED [ 88%]
tests/students/test_courses_api.py::test_course_max_students_limit[21-True] PASSED [100%]

============================== 9 passed in 0.61s ==============================
```

Внутри теста `test_course_max_students_limit[21-True]` проверяется:
- Статус ответа: 400 (Bad Request)
- Ошибка валидации: "Максимум 20 студентов на курсе."


### Сценарий 2: Ошибка в тесте (пример с assert False)

Если в тесте есть ошибка (например, ожидаем 200, а получили 404):

```
============================= test session starts =============================
...
tests/students/test_courses_api.py::test_retrieve_course FAILED          [ 11%]
...
>       assert response.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response status_code=404>.status_code

tests/students/test_courses_api.py:12: AssertionError
=========================== 1 failed, 8 passed in 0.61s ======================
```

### Сценарий 3: Запуск с флагом -v (verbose)

Для подробного вывода:

```
$ pytest -v

============================= test session starts =============================
tests/students/test_courses_api.py::test_retrieve_course PASSED          [ 11%]
tests/students/test_courses_api.py::test_list_courses PASSED             [ 22%]
tests/students/test_courses_api.py::test_filter_courses_by_id PASSED     [ 33%]
tests/students/test_courses_api.py::test_filter_courses_by_name PASSED   [ 44%]
tests/students/test_courses_api.py::test_create_course PASSED            [ 55%]
tests/students/test_courses_api.py::test_update_course PASSED            [ 66%]
tests/students/test_courses_api.py::test_delete_course PASSED            [ 77%]
tests/students/test_courses_api.py::test_course_max_students_limit[20-False] PASSED [ 88%]
tests/students/test_courses_api.py::test_course_max_students_limit[21-True] PASSED [100%]

============================== 9 passed in 0.61s ==============================
```

### Сценарий 4: Запуск конкретного теста

```
$ pytest tests/students/test_courses_api.py::test_create_course -v

============================= test session starts =============================
tests/students/test_courses_api.py::test_create_course PASSED            [100%]

============================== 1 passed in 0.15s ==============================
```

## Дополнительные задания

Выполнено дополнительное задание по ограничению числа студентов на курсе:
- Добавлена валидация в сериализатор
- Добавлен параметр `MAX_STUDENTS_PER_COURSE = 20` в `settings.py`
- Написаны тесты для проверки как успешного сценария (20 студентов), так и ошибочного (21 студент)
