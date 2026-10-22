import sys

import prompt

from primitive_db.utils import load_metadata

from primitive_db.core import create_table

from primitive_db.utils import save_metadata

from primitive_db.core import drop_table

import shlex


def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
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
            case "help":
                print_help()
            case "exit":
                print("Завершаю выполнение программы")
                sys.exit()