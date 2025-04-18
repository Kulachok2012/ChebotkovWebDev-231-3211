import timeit


def fact_rec(n):
    if n == 1:
        return 1
    return n * fact_rec(n - 1)


def fact_it(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


if __name__ == '__main__':
    n = int(input())
    print(fact_rec(n))


'''Рекурсивная версия: 0.00000048 сек за вызов
Итеративная версия: 0.00000031 сек за вызов'''
