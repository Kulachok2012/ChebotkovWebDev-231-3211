n = int(input())
A = input().split()
if len(set(A)) > 1:
    print(sorted(set(A))[-2])
else:
    print("Нет второго элемента")
