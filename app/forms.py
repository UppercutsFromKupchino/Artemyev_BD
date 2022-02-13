from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
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
    text_of_request = StringField(validators=[DataRequired()])
    submit = SubmitField("Оставьте заявку")


class ChangeStatusOfRequestWorker(FlaskForm):
    select_status = SelectField(choices=[])
    hidden_id_of_request = HiddenField()
    changing_submit = SubmitField("Изменить статус заявки")


class ExecuteRequestForWorker(FlaskForm):
    select_executor = SelectField(choices=[])
    hidden_id_of_request = HiddenField()
    changing_submit = SubmitField("Поручить задачу исполнителю")


class SelectProfessionForAWorker(FlaskForm):
    select_worker = SelectField(choices=[])
    select_profession = SelectField(choices=[])
    submit = SubmitField("Добавить профессию")


class AddHabitantFlat(FlaskForm):
    habitant = SelectField(choices=[])
    flat = SelectField(choices=[])
    submit = SubmitField("Добавить квартиру жителю")
