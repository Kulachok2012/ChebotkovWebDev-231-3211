from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # В реальном приложении используйте надёжный ключ

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо войти в систему.'
login_manager.login_message_category = 'info'

# Модель пользователя
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Создадим тестового пользователя
users = [
    User(1, 'user', generate_password_hash('qwerty'))
]

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/')
def home():
    if current_user.is_authenticated:
        flash('Вы успешно вошли в систему!', 'success')
    return render_template('home.html')

@app.route('/visits')
def visits_counter():
    # Увеличиваем счётчик посещений в сессии
    session['visits'] = session.get('visits', 0) + 1
    return render_template('visits.html', visits=session['visits'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Ищем пользователя
        user = next((u for u in users if u.username == username), None)
        
        # Проверяем пароль
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            
            # Перенаправляем на страницу, которую пользователь хотел открыть
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        
        flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)