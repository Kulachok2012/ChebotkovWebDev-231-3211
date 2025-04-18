with open("lab1/products.csv", 'r', encoding='utf-8') as file:
    next(file)

    total_adult = 0.0
    total_senior = 0.0
    total_child = 0.0

    for line in file:
        parts = line.strip().split(',')
        if len(parts) >= 4:  
            adult_expense = float(parts[1].replace(',', ''))
            senior_expense = float(parts[2].replace(',', ''))
            child_expense = float(parts[3].replace(',', ''))
            total_adult += adult_expense
            total_senior += senior_expense
            total_child += child_expense 

    print(f"{total_adult:.2f}{"\n"}{total_senior:.2f}{"\n"}{total_child:.2f}")