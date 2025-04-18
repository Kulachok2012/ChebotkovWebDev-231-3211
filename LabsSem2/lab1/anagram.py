str1 = input()
str2 = input()

str1 = str1.replace(" ", "").lower()
str2 = str2.replace(" ", "").lower()

char_count1 = {}
char_count2 = {}

for char in str1:
    char_count1[char] = char_count1.get(char, 0) + 1

for char in str2:
    char_count2[char] = char_count2.get(char, 0) + 1


if char_count1 == char_count2:
    print("YES")
else:
    print("NO")

