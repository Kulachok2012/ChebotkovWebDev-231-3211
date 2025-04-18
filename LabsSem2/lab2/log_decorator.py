import os
import time
from datetime import datetime

def function_logger(log_file):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Получение текущего времени в указанном формате
            start_time = datetime.now()
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            
            # Логирование названия функции
            log_data = [func.__name__]
            
            # Логирование времени начала выполнения
            log_data.append(start_time_str)
            
            # Логирование входных аргументов
            log_data.append(repr(args))
            log_data.append(repr(kwargs))
            
            # Выполнение функции
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = f"Exception: {e}"
            finally:
                end_time = datetime.now()
                duration = end_time - start_time
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S.%f')
                
                # Добавление результата в логи
                log_data.append(result if result is not None else "-")
                
                # Логирование времени завершения
                log_data.append(end_time_str)
                
                # Логирование продолжительности выполнения
                log_data.append(str(duration))
                
                # Запись в файл
                with open(log_file, 'a') as f:
                    for entry in log_data:
                        f.write(str(entry) + '\n')
                    f.write('\n')  # Разделитель для записи
            
            return result
        return wrapper
    return decorator

# Пример использования
@function_logger('test.log')
def greeting_format(name):
    return f"Hello, {name}!"

greeting_format('John')
