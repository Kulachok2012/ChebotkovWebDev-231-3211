n = int(input())
a = []
b = []
for _ in range(n):
    row = list(map(int, input().split()))
    a.append(row)
for _ in range(n):
    row = list(map(int, input().split()))
    b.append(row)

c = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        for k in range(n):
            c[i][j] += a[i][k] * b[k][j]

for row in c:
    print(*row)