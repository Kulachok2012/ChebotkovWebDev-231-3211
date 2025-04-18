from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/url-params')
def show_url_params():
    return render_template('url_params.html', params=request.args)

@app.route('/headers')
def show_headers():
    return render_template('headers.html', headers=dict(request.headers))

@app.route('/cookies')
def show_cookies():
    return render_template('cookies.html', cookies=request.cookies)

@app.route('/form-data', methods=['GET', 'POST'])
def show_form_data():
    form_data = None
    if request.method == 'POST':
        form_data = request.form
    return render_template('form_data.html', form_data=form_data)

@app.route('/phone-form', methods=['GET', 'POST'])
def phone_form():
    error = None
    phone = None
    formatted_phone = None
    
    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('.', '').replace('+', '')
        
        if not cleaned.isdigit():
            error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы'
        else:
            if len(cleaned) not in (10, 11):
                error = 'Недопустимый ввод. Неверное количество цифр'
            elif cleaned.startswith(('7', '8')) and len(cleaned) != 11:
                error = 'Недопустимый ввод. Неверное количество цифр'
            elif not cleaned.startswith(('7', '8')) and len(cleaned) != 10:
                error = 'Недопустимый ввод. Неверное количество цифр'
            else:
                if len(cleaned) == 11:
                    formatted_phone = f"8-{cleaned[1:4]}-{cleaned[4:7]}-{cleaned[7:9]}-{cleaned[9:]}"
                else:
                    formatted_phone = f"8-{cleaned[0:3]}-{cleaned[3:6]}-{cleaned[6:8]}-{cleaned[8:]}"
    
    return render_template('phone_form.html', 
                         phone=phone,
                         error=error,
                         formatted_phone=formatted_phone)

if __name__ == '__main__':
    app.run(debug=True)