def is_leap(year):
    if year % 4 != 0:
        return False
    elif year % 100 == 0:
        return year % 400 == 0
    else:
        return True


year_str = input()
year = int(year_str)

result = is_leap(year)
print(result)
