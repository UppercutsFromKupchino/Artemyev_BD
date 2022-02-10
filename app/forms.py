from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    login_loginform = StringField(validators=[DataRequired()])
    password_loginform = PasswordField(validators=[DataRequired()])
    submit_loginform = SubmitField("Авторизируйтесь")


class LoginMoreThanOneForm(FlaskForm):

    login_loginform = StringField(validators=[DataRequired()])
    password_loginform = PasswordField(validators=[DataRequired()])
    select_role_field = SelectField(choices=[], validators=[DataRequired()])
    submit_loginform = SubmitField("Авторизируйтесь")


class RegisterForm(FlaskForm):

    number_of_phone_regform = StringField(validators=[DataRequired()])
    password_regform = PasswordField(validators=[DataRequired()])
    email_regform = StringField()
    fio_regform = StringField()
    select_role_regform = SelectField(choices=[], validators=[DataRequired()])
    submit_regform = SubmitField("Зарегистрируйтесь")


class AddRequestForm(FlaskForm):

    number_of_flat = SelectField("Номер квартиры", choices=[])
    number_of_building = SelectField("Номер дома", choices=[])
    text_of_request = StringField(validators=[DataRequired()])
    submit = SubmitField("Оставьте заявку")
