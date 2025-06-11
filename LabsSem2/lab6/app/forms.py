from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(),
        Length(min=5, max=50),
        Regexp(r'^[a-zA-Z0-9]+$', message='Только латинские буквы и цифры')
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp(r'^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d)[^\s]{8,128}$', 
               message='Пароль должен содержать минимум 1 заглавную, 1 строчную букву и 1 цифру')
    ])


class UserCreateForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(),
        Length(min=5, max=50),
        Regexp(r'^[a-zA-Z0-9]+$', message='Только латинские буквы и цифры')
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp(r'^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d)[^\s]{8,128}$', 
               message='Пароль должен содержать минимум 1 заглавную, 1 строчную букву и 1 цифру')
    ])
    
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')


class UserEditForm(FlaskForm):    
    role_id = SelectField('Идентификатор роли', choices=[1, 2])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp(r'^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d)[^\s]{8,128}$',
               message='Пароль должен содержать минимум 1 заглавную, 1 строчную букву и 1 цифру')
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
