n = int(input())
passenger_times = []

for _ in range(n):
    passenger_times.append([int(i) for i in input().split()])

t = int(input())

i = 0

for time in passenger_times:
    if time[0] <= t <= time[1]:
        i += 1

print(i)