import timeit
#четные в квадрат, нечетные в куб
# Версия с List Comprehension: 0.00000054 сек за вызов
def process_list(arr):
    result = [i ** 2 if i % 2 == 0 else i ** 3 for i in arr]
    return result

# Версия-генератор: 0.00000015 сек за вызов
def process_list_gen(arr):
    return (i ** 2 if i % 2 == 0 else i ** 3 for i in arr)

if __name__ == '__main__':
    #
    nums = list(map(int, input().split()))
    
    print(*list(process_list_gen(nums)))

'''Версия с List Comprehension: 0.00000068 сек за вызов
Версия-генератор: 0.00000016 сек за вызов'''
