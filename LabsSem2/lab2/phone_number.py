def wrapper(f):
    def fun(l):
        # Преобразуем каждый номер телефона в стандартный формат
        formatted_numbers = []
        for number in l:
            clean_number = number[-10:]  # Извлекаем последние 10 цифр
            formatted_number = f"+7 ({clean_number[:3]}) {clean_number[3:6]}-{clean_number[6:8]}-{clean_number[8:]}"
            formatted_numbers.append(formatted_number)
        return f(formatted_numbers)
    return fun

@wrapper
def sort_phone(l):
    return sorted(l)

if __name__ == '__main__':
    l = [input() for _ in range(int(input()))]
    print(*sort_phone(l), sep='\n')

'''3
07895462130
89875641230
9195969878'''