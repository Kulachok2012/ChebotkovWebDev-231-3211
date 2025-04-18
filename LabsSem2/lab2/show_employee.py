def show_employee(name, salary=100000):
    return f"{name}: {salary} Р"

if __name__ == '__main__':
    a, b = input(), int(input())
    print(show_employee(a, b))  
    
