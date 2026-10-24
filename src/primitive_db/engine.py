import sys

import prompt

import shlex

from prettytable import PrettyTable

from primitive_db.utils import load_metadata, save_metadata, load_table_data, save_table_data

from primitive_db.core import create_table, drop_table, insert, select, update, delete

from primitive_db.parser import parsing


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу\n")
    print("***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    while True:
        metadata = load_metadata("db_meta.json")
        print_help()
        command = prompt.string("Введите команду: ")
        args = shlex.split(command)
        match args[0]:
            case "create_table":
                table_name = args[1]
                columns = args[2:]
                table = create_table(metadata, table_name, columns)
                if table is not None:
                    save_metadata("db_meta.json", table)
                    print(f"Таблица {table_name} успешно создана!")
            case "list_tables":
                for table_name in metadata:
                    print(table_name)
            case "drop_table":
                table_name = args[1]
                table = drop_table(metadata, table_name)
                if table is not None:
                    save_metadata("db_meta.json", table)
            case "insert":
                 table_name = args[2]
                 values = args[4:]
                 values = [value.strip("(),") for value in values]
                 result = insert(metadata, table_name, values)
                 if result is not None:
                     save_metadata(f"data/{table_name}.json", result)
            case "select":
                table_name = args[2]
                data = load_table_data(table_name)
                if "where" in args:
                    condition = " ".join(args[4:])
                    where_clause = parsing(condition)
                    result = select(data, where_clause)
                else:
                    result = select(data)

                if result:
                    table = PrettyTable()
                    table.field_names = list(result[0].keys())
                    for entry in result:
                        table.add_row(list(entry.values()))
                    print(table)
                else:
                    print("Ничего не найдено!")
            case "update":
                table_name = args[1]
                data = load_table_data(table_name)
                where_index = args.index("where")
                set_condition = " ".join(args[3:where_index])
                where_condition = " ".join(args[where_index + 1:])
                set_clause = parsing(set_condition)
                where_clause = parsing(where_condition)
                result = update(data, set_clause, where_clause)
                print(result)
                save_table_data(table_name, result)
            case "delete":
                table_name = args[2]
                data = load_table_data(table_name)
                where_index = args.index("where")
                where_condition = " ".join(args[where_index + 1:])
                where_clause = parsing(where_condition)
                result = delete(data, where_clause)
                print(result)
                save_table_data(table_name, result)
            case "help":
                print_help()
            case "exit":
                print("Завершаю выполнение программы")
                sys.exit()