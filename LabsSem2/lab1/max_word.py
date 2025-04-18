with open("lab1/example.txt", 'r', encoding='utf-8') as file:
    text = file.read().lower()  

    words = []
    current_word = ""
    for char in text:
        if char.isalpha():
            current_word += char
        elif current_word: 
            words.append(current_word)
            current_word = ""

    if current_word: 
        words.append(current_word)

    max_length = 0
    for word in words:
        max_length = max(max_length, len(word))

    longest_words = [word for word in words if len(word) == max_length]

    for word in longest_words:
        print(word)


