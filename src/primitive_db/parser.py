def parsing(condition):
    """Парсинг на имя и значение"""
    segments = condition.split("=")
    segments = [segment.strip(" ,'\"") for segment in segments]
    result = {}
    if segments[1].isdigit():
      segments[1] = int(segments[1])
    elif segments[1] == "True":
      segments[1] = True
    elif segments[1] == "False":
      segments[1] = False
    result[segments[0]] = segments[1]
    return result