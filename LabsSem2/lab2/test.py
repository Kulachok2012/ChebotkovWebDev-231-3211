import subprocess
import pytest

INTERPRETER = 'python'

def run_script(filename, input_data=None):
    proc = subprocess.run(
        [INTERPRETER, f'./lab2/{filename}'],
        input='\n'.join(input_data if input_data else []),
        capture_output=True,
        text=True,
        check=False
    )
    return proc.stdout.strip()

test_data = {
    'fact': [
        ('5', '120'),
        ('10', '3628800'),
        ('15', '1307674368000'),
        ('20', '2432902008176640000'),
        ('25', '15511210043330985984000000'),
        ('30', '265252859812191058636308480000000'),
        ('35', '10333147966386144929666651337523200000000'),
        ('40', '815915283247897734345611269596115894272000000000')
    ],
    'show_employee': [
        (['Иванов Иван Иванович', '30000'], 'Иванов Иван Иванович: 30000 Р'),
        (['Петров Петр Петрович', '100000'], 'Петров Петр Петрович: 100000 Р'),
        (['Летов Егор', '20000'], 'Летов Егор: 20000 Р'),
        (['Кобейн Курт', '199100'], 'Кобейн Курт: 199100 Р'),
        (['Уильям Шульц', '3500000'], 'Уильям Шульц: 3500000 Р')
    ],
    'sum_and_sub': [
        (['5', '3'], '8 2'),
        (['-5', '3'], '-2 -8'),
        (['-5', '-3'], '-8 -2'),
        (['5', '-3'], '2 8'),
        (['102010201020', '101010101010'], '203020302030 1000100010')
    ],
    'process_list': [
        ('1 2 3 4 5 6 7 8 9 10', '1 4 27 16 125 36 343 64 729 100'),
        ('-1 -2 -3 -4 -5 -6 -7 -8 -9 -10', '-1 4 -27 16 -125 36 -343 64 -729 100'),
        ('1 4 8 8 1 3 3 7 2 2 8', '1 16 64 64 1 27 27 343 4 4 64'),
        ('-1 -4 -8 -8 -3 -3 -7 -2 -2 -8', '-1 16 64 64 -27 -27 -343 4 4 64'),
        ('121 18312 9291 1230 1202', '1771561 335329344 802024029171 1512900 1444804'),
    ],
    'my_sum': [
        ('1 2 3 4 5 6 7 8 9 10', '55'),
        ('-1 -2 -3 -4 -5 -6 -7 -8 -9 -10', '-55'),
        ('1 4 8 8 1 3 3 7 2 2 8', '47'),
        ('-1 -4 -8 -8 -3 -3 -7 -2 -2 -8', '-46'),
        ('121 18312 9291 1230 1202', '30156')
    ],
    'files_sort': [
        ('./lab2/files', ['123.py', 'abc.txt', 'text.txt'])
    ],
    'file_search': [
        ('happiness.py', ['Найден файл: D:\\shkola\\Webdebil\\ChebotkovWebDev-231-3211\\LabsSem2\\lab1\\happiness.py',
                        '',
                        'Первые 5 строк файла:',
                        'n, m = map(int, input().split())',
                        'arr = list(map(int, input().split()))',
                        'a = set(map(int, input().split()))',
                        'b = set(map(int, input().split()))'])
    ],
    'email_validation': [
        (['3', 'lara@mospolytech.ru', 'brian-23@mospolytech.ru', 'britts_54@mospolytech.ru'], 
            "['brian-23@mospolytech.ru', 'britts_54@mospolytech.ru', 'lara@mospolytech.ru']"),
        (['2', 'igor2233balashov@gmail.com', 'tchebotkov.dima@yandex.ru'], 
            "['igor2233balashov@gmail.com', 'tchebotkov.dima@yandex.ru']"),
        (['2', 'kakaxa1805@gmail.yandex', 'kakaxa1805@gmail.com'], 
            "['kakaxa1805@gmail.com']"),
        (['1', 'john_doe@rambler.goy'], 
            "['john_doe@rambler.goy']"),
        (['3', 'john_doe@rambler.goyda', 'john_doe@ram-bler.goy', 'john_doe@rambler.goy'], 
            "['john_doe@rambler.goy']"),
    ],
    'fibonacci': [
        ('1', '0'),
        ('2', '0 1'),
        ('3', '0 1 1'),
        ('4', '0 1 1 8'),
        ('5', '0 1 1 8 27'),
        ('6', '0 1 1 8 27 125'),
        ('7', '0 1 1 8 27 125 512'),
        ('8', '0 1 1 8 27 125 512 2197'),
        ('9', '0 1 1 8 27 125 512 2197 9261'),
        ('10', '0 1 1 8 27 125 512 2197 9261 39304'),
        ('11', '0 1 1 8 27 125 512 2197 9261 39304 166375'),
        ('12', '0 1 1 8 27 125 512 2197 9261 39304 166375 704969'),
        ('13', '0 1 1 8 27 125 512 2197 9261 39304 166375 704969 2985984'),
        ('14', '0 1 1 8 27 125 512 2197 9261 39304 166375 704969 2985984 12649337'),
        ('15', '0 1 1 8 27 125 512 2197 9261 39304 166375 704969 2985984 12649337 53582633')
    ],
    'average_scores': [
            (['5 3', '89 90 78 93 80', '90 91 85 88 86', '91 92 83 89 90.5'], ['90.0', '91.0', '82.0', '90.0', '85.5'])
        ],
        'plane_angle': [
        (['0 0 0', '1 0 0', '1 1 0', '1 1 1'], '90.00'),
        (['-1 0 0', '1 0 0', '-1 1 0', '1 1 1'], '48.19'),
        (['4 5 6', '1 2 3', '1 4 8', '2 2 8'], '89.18'),
        (['0 -1 0', '-1 0 0', '0 0 -1', '0 0 0'], '125.26'),
        (['0.5 21 3', '-1 6 8', '-123 3 2', '10 123 -9'], '169.83')
    ],
    'phone_number': [
        (['3', '07895462130', '89875641230', '9195969878'], 
            ['+7 (789) 546-21-30', '+7 (919) 596-98-78', '+7 (987) 564-12-30']),
        (['4', '07895362230', '89815631250', '9195369832', '89324532312'], 
            ['+7 (789) 536-22-30', '+7 (919) 536-98-32', '+7 (932) 453-23-12', '+7 (981) 563-12-50'])
    ],
    'people_sort': [
        (['3', 'Mike Thomson 20 M', 'Robert Bustle 32 M', 'Andria Bustle 30 F'], 
            ['Mr. Mike Thomson', 'Ms. Andria Bustle', 'Mr. Robert Bustle'])
    ],
    'complex_numbers': [
        (['2 1', '5 6'], ['7.00+7.00i', '-3.00-5.00i', '4.00+17.00i', '0.26-0.11i', '2.24+0.00i', '7.81+0.00i'])
    ]
}


@pytest.mark.parametrize('input_data, expected', test_data['fact'])
def test_fact(input_data, expected):
    assert run_script('fact.py', [input_data]) == expected

@pytest.mark.parametrize('input_data, expected', test_data['show_employee'])
def test_show_employee(input_data, expected):
    assert run_script('show_employee.py', input_data) == expected

@pytest.mark.parametrize('input_data, expected', test_data['sum_and_sub'])
def test_sum_and_sub(input_data, expected):
    assert run_script('sum_and_sub.py', input_data) == expected

@pytest.mark.parametrize('input_data, expected', test_data['process_list'])
def test_process_list(input_data, expected):
    assert run_script('process_list.py', [input_data]) == expected

@pytest.mark.parametrize('input_data, expected', test_data['my_sum'])
def test_my_sum(input_data, expected):
    assert run_script('my_sum.py', [input_data]) == expected

@pytest.mark.parametrize('input_data, expected', test_data['files_sort'])
def test_files_sort(input_data, expected):
    assert run_script('files_sort.py', [input_data]).split('\n') == expected

@pytest.mark.parametrize('input_data, expected', test_data['file_search'])
def test_file_search(input_data, expected):
    assert run_script('file_search.py', [input_data]).split('\n') == expected

@pytest.mark.parametrize('input_data, expected', test_data['email_validation'])
def test_email_validation(input_data, expected):
    assert run_script('email_validation.py', input_data) == expected
    
@pytest.mark.parametrize('input_data, expected', test_data['fibonacci'])
def test_fibonacci(input_data, expected):
    assert run_script('fibonacci.py', [input_data]) == expected

@pytest.mark.parametrize('input_data, expected', test_data['average_scores'])
def test_average_scores(input_data, expected):
    assert run_script('average_scores.py', input_data).split('\n') == expected

@pytest.mark.parametrize('input_data, expected', test_data['plane_angle'])
def test_plane_angle(input_data, expected):
    assert run_script('plane_angle.py', input_data) == expected

@pytest.mark.parametrize('input_data, expected', test_data['phone_number'])
def test_phone_number(input_data, expected):
    assert run_script('phone_number.py', input_data).split('\n') == expected

@pytest.mark.parametrize('input_data, expected', test_data['people_sort'])
def test_people_sort(input_data, expected):
    assert run_script('people_sort.py', input_data).split('\n') == expected

@pytest.mark.parametrize('input_data, expected', test_data['complex_numbers'])
def test_complex_numbers(input_data, expected):
    assert run_script('complex_numbers.py', input_data).split('\n') == expected
