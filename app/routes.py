from app import app
from flask import render_template, redirect, url_for, flash, g, session
from app.DataBase import DataBase
from app.forms import LoginForm, RegisterForm, AddRequestForm, LoginMoreThanOneForm
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import psycopg2.errors
import datetime


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="Artemyev_BD", user="postgres", password="alp37327", host="localhost")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# Создание объекта для работы с бд
@app.before_request
def before_request():
    db = get_db()
    global dbase
    dbase = DataBase(db)


# Закрытие работы с базой данных
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Проверка на аутентификацию пользователя
    if 'loggedin' in session:
        return redirect(url_for('home'))

    login_form = LoginForm()

    # Проверка на валидацию формы
    if login_form.submit_loginform.data:

        password = login_form.password_loginform.data
        users = dbase.get_users_password_on_login(login_form.login_loginform.data)

        if not users:

            flash('Пользователя с таким номером телефона не существует')
            return redirect(url_for('login'))

        elif users:

            users_len = len(users)

            if users_len == 1:
                password_hash = str(users[0][1])

                if check_password_hash(password_hash, password):

                    session['loggedin'] = True
                    session['id_of_user'] = users[0][0]
                    session['id_of_role'] = users[0][2]
                    return redirect(url_for('home'))

                else:

                    flash('Вы ввели неверный пароль')
                    return redirect(url_for('login'))

            elif users_len > 1:

                login_more_than_one_form = LoginMoreThanOneForm()

                login_more_than_one_form.select_role_field.choices = \
                    dbase.get_users_roles_on_login(login_form.login_loginform.data)

                if login_more_than_one_form.validate_on_submit():

                    user = dbase.get_user_on_role_and_phone(login_more_than_one_form.login_loginform.data,
                                                            login_more_than_one_form.select_role_field.data)

                    if check_password_hash(user[1], login_more_than_one_form.password_loginform.data):

                        session['loggedin'] = True
                        session['id_of_user'] = user[0]
                        session['id_of_role'] = user[2]
                        return redirect(url_for('home'))

                return render_template("login.html", login_more_than_one_form=login_more_than_one_form,
                                       users_len_more=True)

    return render_template("login.html", login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegisterForm()
    regform.select_role_regform.choices = dbase.get_roles()
    print(regform.select_role_regform.choices)

    if regform.validate_on_submit():

        _hashed_password = generate_password_hash(regform.password_regform.data)
        user = dbase.get_user(regform.number_of_phone_regform.data, regform.select_role_regform.data)

        if user:

            flash('Такой пользователь уже существует!')
            return redirect(url_for('login'))

        else:

            dbase.add_user(regform.number_of_phone_regform.data, regform.email_regform.data,
                           regform.fio_regform.data, _hashed_password, regform.select_role_regform.data)

            if regform.select_role_regform.data == '1':

                users_id = dbase.get_users_id(regform.number_of_phone_regform.data, regform.select_role_regform.data)
                dbase.add_habitant(users_id[0])
                return redirect(url_for('login'))

    return render_template("register.html", regform=regform)


@app.route('/request', methods=['GET', 'POST'])
def request():
    if 'loggedin' not in session:
        return redirect(url_for('home'))
    elif session['role'] == "habitant":

        add_request_form = AddRequestForm()

        add_request_form.number_of_building.choices = dbase.get_all_buildings()
        add_request_form.number_of_flat.choices = dbase.get_all_flats()

        if add_request_form.validate_on_submit():

            id_of_habitant = session['id_of_habitant']
            id_of_flat = dbase.get_id_of_flat(add_request_form.number_of_building.data,
                                              add_request_form.number_of_flat.data)
            print(id_of_flat)
            current_datetime = datetime.datetime.now()
            dbase.add_request(id_of_habitant,
                              id_of_flat[0],
                              current_datetime,
                              add_request_form.text_of_request.data)
        return render_template("request.html", add_request_form=add_request_form)
    elif session['role'] == "worker":

        return render_template("request.html")


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('role', None)
    session.clear()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('home'))
