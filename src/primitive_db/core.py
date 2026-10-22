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