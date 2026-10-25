import time


def handle_db_errors(func):
    """Обработка ошибок"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. "
                  "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper


def confirm_action(action_name):
    """Подтверждение опасных действий"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if answer == "y":
              return func(*args, **kwargs)
            else:
              return None
        return wrapper
    return decorator


def log_time(func):
    """Измерение времени выполнения функций"""
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        operation_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {operation_time:.3f} секунд")
        return result
    return wrapper


def create_cacher():
    """Создание замыкания для кэширования"""
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        else:
            result = value_func()
            cache[key] = result
            return result
    return cache_result