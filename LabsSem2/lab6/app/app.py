from datetime import datetime, UTC
import re
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from lab6.app.forms import LoginForm, UserCreateForm, UserEditForm, ChangePasswordForm

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    
    role = db.relationship('Role', backref='users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validate_login(login):
    if len(login) < 5:
        return False, 'Логин должен содержать не менее 5 символов'
    if not re.match(r'^[a-zA-Z0-9]+$', login):
        return False, 'Логин должен содержать только латинские буквы и цифры'
    return True, ''


def validate_password(password):
    errors = []
    if len(password) < 8 or len(password) > 128:
        errors.append('Длина пароля должна быть от 8 до 128 символов')
    if not re.search(r'[A-ZА-Я]', password):
        errors.append('Должна быть хотя бы одна заглавная буква')
    if not re.search(r'[a-zа-я]', password):
        errors.append('Должна быть хотя бы одна строчная буква')
    if not re.search(r'\d', password):
        errors.append('Должна быть хотя бы одна цифра')
    if re.search(r'\s', password):
        errors.append('Пароль не должен содержать пробелов')
    if not re.match(r'^[a-zA-Zа-яА-Я0-9~!?@#$%^&*_\-+()\[\]{}><\/\\|\'.,:;]+$', password):
        errors.append('Содержатся недопустимые символы')
    return len(errors) == 0, ', '.join(errors)


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        try:
            user = User(
                login=form.login.data,
                password_hash=generate_password_hash(form.password.data)
            )
            print(generate_password_hash(form.password.data))
            user = User.query.filter_by(login=user.login).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка входа: {str(e)}', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = UserCreateForm()  
    
    if form.validate_on_submit():
        try:
            user = User(
                login=form.login.data,
                password_hash=generate_password_hash(form.password.data),
                last_name=form.last_name.data,
                first_name=form.first_name.data,
                middle_name=form.middle_name.data,
                role_id=1
            )
            db.session.add(user)
            db.session.commit()
            flash('Пользователь успешно создан!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка создания пользователя: {str(e)}', 'danger')
    
    return render_template('create_user.html', form=form)  # Передаем форму в шаблон


@app.route('/user/<int:user_id>')
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    return render_template('view_user.html', user=user, roles=roles)


@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(user)
            db.session.commit()
            flash('Изменения сохранены', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при обновлении: {str(e)}', 'danger')
        return redirect(url_for('index'))
    roles = Role.query.all()
    return render_template('user_form.html', form=form, user=user, roles=roles)


@app.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка удаления: {str(e)}', 'danger')
    return redirect(url_for('index'))


@app.route('/user/<int:user_id>/change-password', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user = User.query.get_or_404(user_id)
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not check_password_hash(user.password_hash, form.old_password.data):
            flash('Неверный старый пароль', 'danger')
        elif form.new_password.data != form.confirm_password.data:
            flash('Новые пароли не совпадают', 'danger')
        else:
            try:
                user.password_hash = generate_password_hash(form.new_password.data)
                db.session.commit()
                flash('Пароль успешно изменен', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка изменения пароля: {str(e)}', 'danger')
    return render_template('change_password.html', form=form, user=user)


if __name__ == '__main__':
    app.run(debug=True)
    
   
