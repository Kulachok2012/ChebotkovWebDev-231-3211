import operator

def person_lister(f):
    def inner(people):
        # Сортируем список по возрасту (поле person[2], преобразованное в int)
        return map(f, sorted(people, key=lambda x: int(x[2])))
    return inner

@person_lister
def name_format(person):
    # Форматируем вывод в зависимости от пола
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]

if __name__ == '__main__':
    # Ввод данных: количество людей и их параметры
    people = [input().split() for i in range(int(input()))]
    print(*name_format(people), sep='\n')

"""3
Mike Thomson 20 M
Robert Bustle 32 M
Andria Bustle 30 F"""