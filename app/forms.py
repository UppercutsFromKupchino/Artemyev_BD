from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login_loginform = StringField("Введите логин", validators=[DataRequired()])
    password_loginform = PasswordField("Введите пароль", validators=[DataRequired()])
    submit_loginform = SubmitField("Авторизируйтесь")


class RegisterForm(FlaskForm):
    number_of_phone_regform = StringField("Номер телефона", validators=[DataRequired()])
    password_regform = PasswordField("Пароль", validators=[DataRequired()])
    email_regform = StringField("email")
    fio_regform = StringField("ФИО", validators=[DataRequired()])
    submit_regform = SubmitField("Зарегистрируйтесь")


class AddRequestForm(FlaskForm):
    number_of_flat = SelectField()
    number_of_building = SelectField()
    text_of_request = StringField(validators=[DataRequired()])
    submit = SubmitField()
