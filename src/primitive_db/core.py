import json

from primitive_db.constants import VALID_TYPES
from primitive_db.decorators import (
  confirm_action,
  create_cacher,
  handle_db_errors,
  log_time,
)
from primitive_db.utils import load_table_data

cached = create_cacher()

@handle_db_errors
def create_table(metadata, table_name, columns):
  """Создание таблицы"""
  if table_name in metadata:
    print(f"Таблица {table_name} уже существует!")
    return None
  columns_with_id = ['ID:int'] + columns
  column_types = []
  for column in columns_with_id:
    columns_separated = column.split(':')
    column_types.append(columns_separated[1])
  if all(item in VALID_TYPES for item in column_types):
    metadata[table_name] = {"columns": columns_with_id}
    return metadata
  else:
    print("Некорректный тип данных")
    return None


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
  """Удаление таблицы"""
  if table_name not in metadata:
    print(f"Таблица {table_name} отсутствует!")
    return None
  
  del metadata[table_name]
  print(f"Таблица {table_name} успешно удалена!")

  return metadata

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
  """Добавление данных в таблицу"""
  if table_name not in metadata:
    print(f"Таблица {table_name} не существует!")
    return None
  columns = metadata[table_name]["columns"]
  if len(columns) - 1 != len(values):
    print("Количество переданных значений не соответствует количеству столбцов")
    return None
  values_converted = []

  for column, value in zip(columns[1:], values):
    column_name, column_type = column.split(":")
    if column_type == "int":
      value = int(value)
    elif column_type == "bool":
      if value.lower() == "true":
        value = True
      elif value.lower() == "false":
        value = False
      else:
        print(f"Значение {column_name} должно быть true или false")
        return None
    values_converted.append(value)


  data = load_table_data(table_name)

  if not data:
    data = []

  new_id = len(data) + 1

  new_entry = {"ID": new_id}

  for column, value in zip(columns[1:], values_converted):
    column_name = column.split(":")[0]
    new_entry[column_name] = value

  data.append(new_entry)
  return data

@handle_db_errors
@log_time
def select(table_data, where_clause=None):
  """Выбор записей из таблицы по заданному условию"""
  cache_key = json.dumps([table_data, where_clause], sort_keys=True)

  def get_result():
    if where_clause is None:
        return table_data
    else:
      result = []
      clause = where_clause
      key = list(clause.keys())[0]
      value = list(clause.values())[0]
      for table in table_data:
        if table[key] == value:
          result.append(table)
      return result
  return cached(cache_key, get_result)

@handle_db_errors
def update(table_data, set_clause, where_clause):
  """Обновление таблицы"""
  clause = where_clause
  clause_for_update = set_clause
  key = list(clause.keys())[0]
  value = list(clause.values())[0]
  new_key = list(clause_for_update.keys())[0]
  new_value = list(clause_for_update.values())[0]
  for table in table_data:
    if table[key] == value:
        table[new_key] = new_value
  return table_data

@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
  """Удаление таблицы"""
  clause = where_clause
  key = list(clause.keys())[0]
  value = list(clause.values())[0]
  result = []
  for table in table_data:
    if table[key] != value:
      result.append(table)
  return result



  