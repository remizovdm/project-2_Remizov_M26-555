from primitive_db.utils import load_table_data


def create_table(metadata, table_name, columns):
  valid_types = ('int','str','bool')
  if table_name in metadata:
    print(f"Таблица {table_name} уже существует!")
    return None
  columns_with_id = ['ID:int'] + columns
  column_types = []
  for column in columns_with_id:
    columns_separated = column.split(':')
    column_types.append(columns_separated[1])
  if all(item in valid_types for item in column_types):
    metadata[table_name] = {"columns": columns_with_id}
    return metadata
  else:
    print(f"Некорректный тип данных")
    return None


def drop_table(metadata, table_name):
  if table_name not in metadata:
    print(f"Таблица {table_name} отсутствует!")
    return None
  
  del metadata[table_name]
  print(f"Таблица {table_name} успешно удалена!")

  return metadata


def insert(metadata, table_name, values):
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
      try:
        value = int(value)
      except ValueError:
        print(f"Значение {column_name} должно быть целым числом")
        return None
    elif column_type == "bool":
      if value.lower() == "true":
        value = True
      elif value.lower() == "false":
        value = False
      else:
        print(f"Значение {column_name} должно быть true или false")
        return None
    values_converted.append(value)


  filepath = f"data/{table_name}.json"
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


def select(table_data, where_clause=None):
  if where_clause == None:
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


def update(table_data, set_clause, where_clause):
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


def delete(table_data, where_clause):
  clause = where_clause
  key = list(clause.keys())[0]
  value = list(clause.values())[0]
  result = []
  for table in table_data:
    if table[key] != value:
      result.append(table)
  return result



  