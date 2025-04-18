word = input("")

vowels = "AEIOUY"  
consonant_count = 0
vowel_count = 0

for i in range(len(word)):
    if word[i] in vowels:
        vowel_count += len(word) - i  
    else:
        consonant_count += (
            len(word) - i
        ) 

if consonant_count > vowel_count:
    print("Стюарт", consonant_count)
elif vowel_count > consonant_count:
    print("Кевин", vowel_count)
else:
    print("Ничья")
