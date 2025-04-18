import os

def list_files_by_extension(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()

    extensions = sorted(list(set([f.split('.')[-1] for f in files])))

    for ext in extensions:
        for file in files:
            if file.endswith(f'.{ext}'):
                print(file)

if __name__ == "__main__":
    directory_path = input("")

    if not os.path.isdir(directory_path):
        print("Ошибка: Указанный путь не является директорией.")
        exit(1)

    list_files_by_extension(directory_path)