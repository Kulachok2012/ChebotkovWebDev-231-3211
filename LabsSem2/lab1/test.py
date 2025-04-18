import subprocess
import pytest

INTERPRETER = 'python'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, f'./lab1/{filename}'],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'python_if_else': [
        ('1', 'Weird'),
        ('4', 'Not Weird'),
        ('3', 'Weird'),
        ('6','Weird'),
        ('22', 'Not Weird')
    ],
    'arithmetic_operators': [
        (['1', '2'], ['3', '-1', '2']),
        (['10', '5'], ['15', '5', '50']),
        (['9', '1'], ['10', '8', '9']),
        (['6', '-3'], ['3', '9', '-18']),
        
    ],
    'division': [
        (['5', '2'], ['2', '2.5']),
        (['10', '5'], ['2', '2.0']),
        (['0', '2'], ['0', '0.0']),
        (['1', '2'], ['0', '0.5'])
    ],
    'loops' : [
        (['2'], ['0', '1']),
        (['3'], ['0', '1', '4']),
        (['4'], ['0', '1', '4', '9']),
        (['5'], ['0', '1', '4', '9', '16'])
    ],
    "print_function": [
        (["5"], "12345"),
        (["10"], "12345678910"),
        (["3"], "123"),
        (["7"], "1234567")
    ],
    "second_score": [
        (["5", "2 3 6 6 5"], "5"),
        (["7", "15 13 11 10 15 13 11"], "13"),
        (["3", "10 11 12"], "11")
    ],
    "nested_list": [
        (["3", "Lena", "3", "Leha", "5", "Vova", "4"], "Vova"),
        (["4", "Lena", "3", "Leha", "5", "Vova", "4", "Egor", "4"], "Egor\nVova")
    ],
    "lists": [
        (["5", "insert 1 10", "insert 0 5", "print"], "[5, 10]"),
        (["3", "append 1", "append 2", "print"], "[1, 2]"),
        (["4", "append 10", "append 15", "remove 10", "print"], "[15]"),
        (["5", "insert 1 10", "insert 0 5", "remove 5", "print"], "[10]"),
    ],
    "swap_case": [
        ("HELLO", "hello"),
        ("abcDeF123", "ABCdEf123"),
        ("", ""),
        ("!@#", "!@#"),
        ("asdasasd", "ASDASASD")
    ],
    "split_and_join": [
        ("this is a string", "this-is-a-string"),
        ("1 # @ #", "1-#-@-#"),
        ("12 2 3 1", "12-2-3-1")
    ],
    "max_word": [
        (["example.txt"], "сосредоточенности")
    ],
    "price_sum": [
        (["products.csv"], "6842.84\n5891.06\n6810.90")
    ],
    "anagram": [
        (["lalka", "kaall"], "YES"),
        (["puppy", "taras"], "NO"),
        (["oves", "esvo"], "YES"),
        (["a", "p"], "NO"),
        (["car", "ra"], "NO"),
    ],
      "metro": [
        (["5", "30 35", "15 26", "25 75", "30 59", "12 61", "35"], "4"),
        (["4", "15 20", "20 35", "41 56", "10 60", "21"], "2")
    ],
    "minion_game": [
        (["banana"], "Стюарт 21"),
        (["Minion"], "Стюарт 21"),
        (["Gilbert"], "Стюарт 28")
    ],
    "is_leap": [
        ("1951", "False"),
        ("2024", "True"),
        ("2004", "True"),
        ("1900", "False"),
        ("2100", "False")
    ],

    "happiness": [
        (["12 5","16 41 52 37 89 41 25 67 12 23 45 65","16 20 52 23 40","17 41 65 47 12"],"-1",),
        (["4 2", "10 20 30 40", "10 30", "20 40"], "0"),
        (["3 3", "100 200 300", "100 200 300", "400 500 600"], "3"),
        (["3 3", "10 20 30", "40 50 60", "10 20 30"], "-3"),
        (["1 1", "100", "200", "300"], "0"),
    ],
    "pirate_ship": [(["500 4", "золото 100 1500", "серебро 70 20000", "бананы 400 15000", "металл 150 30000",],"серебро 70.00 20000.00\nметалл 150.00 30000.00\nбананы 280.00 10500.00"),
    ],
    "matrix_mult": [
        (["2", "1 2", "3 4", "5 6", "7 8"], "19 22\n43 50"),
        (["3", "1 2 3", "4 5 5", "3 2 1", "1 2 2", "3 3 3", "5 4 6"], "22 20 26\n44 43 53\n14 16 18"),
    ],
}

def test_hello_world():
    assert run_script('hello.py') == 'Hello, world!'

@pytest.mark.parametrize("input_data, expected", test_data['python_if_else'])
def test_python_if_else(input_data, expected):
    assert run_script('python_if_else.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['arithmetic_operators'])
def test_arithmetic_operators(input_data, expected):
    assert run_script('arithmetic_operators.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['division'])
def test_division(input_data, expected):
    assert run_script('division.py', input_data).split('\n') == expected
    
@pytest.mark.parametrize("input_data, expected", test_data['loops'])
def test_loops(input_data, expected):
    assert run_script('loops.py', input_data).split('\n') == expected

@pytest.mark.parametrize("input_data, expected", test_data['print_function'])
def test_print_function(input_data, expected):
    assert run_script('print_function.py', input_data) == expected
    
@pytest.mark.parametrize("input_data, expected", test_data['second_score'])
def test_second_score(input_data, expected):
    assert run_script('second_score.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['nested_list'])
def test_nested_list(input_data, expected):
    assert run_script('nested_list.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['lists'])
def test_lists(input_data, expected):
    assert run_script('lists.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['swap_case'])
def test_swap_case(input_data, expected):
    assert run_script('swap_case.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['max_word'])
def test_max_word(input_data, expected):
    assert run_script('max_word.py', input_data) == expected
    
@pytest.mark.parametrize("input_data, expected", test_data['price_sum'])
def test_price_sum(input_data, expected):
    assert run_script('price_sum.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['anagram'])
def test_anagram(input_data, expected):
    assert run_script('anagram.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['metro'])
def test_metro(input_data, expected):
    assert run_script('metro.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['minion_game'])
def test_minion_game(input_data, expected):
    assert run_script('minion_game.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['is_leap'])
def test_is_leap(input_data, expected):
    assert run_script('is_leap.py', [input_data]) == expected

@pytest.mark.parametrize("input_data, expected", test_data['happiness'])
def test_happiness(input_data, expected):
    assert run_script('happiness.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['pirate_ship'])
def test_pirate_ship(input_data, expected):
    assert run_script('pirate_ship.py', input_data) == expected

@pytest.mark.parametrize("input_data, expected", test_data['matrix_mult'])
def test_matrix_mult(input_data, expected):
    assert run_script('matrix_mult.py', input_data) == expected

    