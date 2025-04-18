
n, m = map(int, input().split())
items = []

for _ in range(m):
    name, weight, value = input().split()
    weight = int(weight)
    value = int(value)
    items.append((name, weight, value))

items.sort(key=lambda x: x[2] / x[1], reverse=True)

total_weight = 0
result = []

for name, weight, value in items:
    if total_weight + weight <= n:
        total_weight += weight
        result.append((name, weight, value))
    else:
        remaining_weight = n - total_weight
        fraction_value = (value / weight) * remaining_weight
        total_weight += remaining_weight
        result.append((name, remaining_weight, round(fraction_value)))
        break

for name, weight, value in result:
    print(f"{name} {weight:.2f} {value:.2f}")

#50 3
#золото 10 500
#серебро 20 300
#бриллианты 30 900