from datetime import datetime, UTC
import re
from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from lab7.app.forms import LoginForm, UserCreateForm, UserEditForm, ChangePasswordForm

app = Flask(__name__)
app.secret_key = 'f33981eb2946ad39aa14f2298377126f'
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


class VisitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    user = db.relationship('User', backref='visit_logs')


def check_rights(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role.id not in allowed_roles:
                flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapper
    return decorator


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Валидация
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


@app.before_request
def log_visit():
    if request.endpoint and request.endpoint != 'static':
        visit = VisitLog(
            path=request.path,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(visit)
        db.session.commit()


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Создаем экземпляр формы

    if form.validate_on_submit():
        try:
            user = User(
                login=form.login.data,
                password_hash=generate_password_hash(form.password.data)
            )
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
    
    form = UserCreateForm()  # Создаем экземпляр формы
    
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
    
    if current_user.role.id != 2 and current_user.id != user_id:
        flash('У вас недостаточно прав', 'danger')
        return redirect(url_for('index'))
    
    form = UserEditForm(obj=user)
    
    if current_user.role.id != 2:
        form.role_id.render_kw = {'disabled': True}
    
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
@check_rights(2)
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
    
    if current_user.id != user.id and current_user.role.id != 2:
        flash('У вас недостаточно прав', 'danger')
        return redirect(url_for('index'))
    
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


@app.route('/visit-logs')
@login_required
def visit_logs():
    page = request.args.get('page', 1, type=int)
    
    if current_user.role.id == 2:
        logs = VisitLog.query.order_by(VisitLog.created_at.desc()).paginate(page=page, per_page=10)
    else:
        logs = VisitLog.query.filter_by(user_id=current_user.id)\
               .order_by(VisitLog.created_at.desc())\
               .paginate(page=page, per_page=10)
               
    return render_template('visit_logs.html', logs=logs)


@app.route('/page-stats')
@login_required
@check_rights(2)
def page_stats():
    stats = db.session.query(
        VisitLog.path,
        db.func.count(VisitLog.id).label('visits')
    ).group_by(VisitLog.path).order_by(db.desc('visits')).all()
    
    return render_template('page_stats.html', stats=stats)


@app.route('/user-stats')
@login_required
@check_rights(2)
def user_stats():
    stats = db.session.query(
        User,
        db.func.count(VisitLog.id).label('visits')
    ).outerjoin(VisitLog, User.id == VisitLog.user_id).group_by(User.id).order_by(db.desc('visits')).all()
    
    return render_template('user_stats.html', stats=stats)


@app.route('/export-csv/<report_type>')
def export_csv(report_type):
    if report_type == 'page':
        stats = db.session.query(
            VisitLog.path,
            db.func.count(VisitLog.id).label('visits')
        ).group_by(VisitLog.path).order_by(db.desc('visits')).all()
        csv_data = 'Page, Visits\n'
        for stat in stats:
            csv_data += f'{stat.path},{stat.visits}\n'
    elif report_type == 'user':
        stats = db.session.query(
            User,
            db.func.count(VisitLog.id).label('visits')
        ).outerjoin(VisitLog, User.id == VisitLog.user_id).group_by(User.id).order_by(db.desc('visits')).all()
        csv_data = 'User,Visits\n'
        for stat in stats:
            print(stat)
            csv_data += f'{stat[0].login},{stat.visits}\n'
    
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-disposition': f'attachment; filename={report_type}_report.csv'}
    )


if __name__ == '__main__':
    app.run(debug=True)
