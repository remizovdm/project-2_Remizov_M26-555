import json

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загрузка метаданных"""
    try:
        with open(filepath) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохранение метаданных"""
    with open(filepath, "w") as file:
        json.dump(data, file)


def load_table_data(table_name):
    """Загрузка записей таблицы"""
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath) as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

def save_table_data(table_name, data):
    """Сохранение записей таблицы"""
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w") as file:
        json.dump(data, file)