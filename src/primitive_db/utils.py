import json


def load_metadata(filepath):
    try:
        with open(filepath) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file)


def load_table_data(table_name):
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath) as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    

def save_table_data(table_name, data):
    filepath = f"data/{table_name}.json"
    with open(filepath, "w") as file:
        json.dump(data, file)