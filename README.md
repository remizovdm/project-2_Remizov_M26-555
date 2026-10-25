# project-2_Remizov_M26-555
ОПИСАНИЕ ПРОЕКТА
Проект database позволяет работать в консоли с примитивными базами данных в формате JSON.
Можно создавать и удалять таблицы данных, добавлять и редактировать данные, выбирать записи по заданным условиям.

УСТАНОВКА ЗАВИСИМОСТЕЙ
uv sync

ЗАПУСК ПРОЕКТА
uv run database

Демонстрация полного сценария работы с базой данных:
https://asciinema.org/a/d5aaK8JnJ710qwfd

УПРАВЛЕНИЕ ТАБЛИЦАМИ

Создание таблицы:
Команда create_table <имя_таблицы> <столбец1:тип> <столбец2:тип>...
Пример использования:
create_table students name:str age:int passed_the_test:bool

Показать список всех таблиц:
Команда list_tables

Удалить существующую таблицу:
Команда drop_table <имя_таблицы>
Пример использования:
drop_table students

https://asciinema.org/a/7y3r3npWdePgXyGj


CRUD-ОПЕРАЦИИ

Создание записи:
Команда insert into <имя_таблицы> values (<значение1>, <значение2>, ...)
Пример использования:
insert into users values ('John', 30, True)

Чтение записей по условию:
Команда select from <имя_таблицы> where <столбец> = <значение>
Пример использования:
select from users where is_active = True

Чтение всех записей:
Команда select from <имя_таблицы>
Пример использования:
select from users

Обновление записи:
Команда update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>
Пример использования:
update users set age = 41 where age = 42

Удаление записи:
Команда delete from <имя_таблицы> where <столбец> = <значение>
Пример использования:
delete from users where age = 41

https://asciinema.org/a/qjV1rROLBykQDT0L


НОВЫЕ ВОЗМОЖНОСТИ:
Декоратор handle_db_errors перехватывает основные ошибки (KeyError, ValueError и FileNotFoundError) и выводит соответствующие сообщения об ошибках.
Декоратор confirm_action запрашивает у пользователя подтверждение для опасных операций (удаление таблиц и записей).
Декоратор log_time замеряет время выполнения функций select и insert и выводит его в консоль.
Функция create_cacher интегрирована в операцию select и позволяет кэшировать результаты одинаковых запросов.

https://asciinema.org/a/2SCLEijZfV9JhcAE


