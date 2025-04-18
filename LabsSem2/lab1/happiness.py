n, m = map(int, input().split())
arr = list(map(int, input().split()))
a = set(map(int, input().split()))
b = set(map(int, input().split()))

mood = 0
for num in arr:
    if num in a:
        mood += 1
    elif num in b:
        mood -= 1

print(mood)
