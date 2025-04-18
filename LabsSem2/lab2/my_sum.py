def my_sum(*args):
    
    total = 0
    for number in args:
        total += number
    return total

if __name__ == '__main__':
    nums = list(map(int, input().split()))
    result = my_sum(*nums) 
    print(result)