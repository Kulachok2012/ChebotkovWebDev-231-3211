import os

def find_file(filename, directory):
    for root, _, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def print_first_lines(filepath, num_lines=5):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= num_lines:
                    break
                print(line, end='')
    except FileNotFoundError:
        print(f"Файл '{filepath}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")

if __name__ == "__main__":
    
    filename = input()
    
    # Получаем текущую директорию
    current_directory = os.getcwd()
    
    # Ищем файл
    filepath = find_file(filename, current_directory)

    if filepath:
        print(f"\nНайден файл: {filepath}")
        print("\nПервые 5 строк файла:")
        print_first_lines(filepath)
    else:
        print(f"\nФайл '{filename}' не найден.")


# & d:/shkola/Webdebil/ChebotkovWebDev-231-3211/LabsSem2/.venv/Scripts/python.exe d:/shkola/Webdebil/ChebotkovWebDev-231-3211/LabsSem2/lab2/file_search.py metro.py