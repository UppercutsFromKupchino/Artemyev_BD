from app import app
from flask import render_template, redirect, url_for, flash, g, session
from app.DataBase import DataBase
from app.forms import LoginForm, RegisterForm, AddRequestForm
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import psycopg2.errors


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
    if login_form.validate_on_submit():
        user = dbase.get_user(login_form.login_loginform.data)
        admin = dbase.get_admin(login_form.login_loginform.data)
        print(user)
        # Проверка на user
        if user and check_password_hash(user[3], login_form.password_loginform.data):
            session['loggedin'] = True
            habitant = dbase.get_habitant(login_form.login_loginform.data)
            if habitant:
                session['role'] = "habitant"
                redirect(url_for('home'))
            else:
                worker = dbase.get_worker(login_form.login_loginform.data)
                if worker:
                    session['role'] = "worker"
                    redirect(url_for('home'))
        # Проверка на admin
        elif admin and check_password_hash(admin[1], login_form.password_loginform.data):
            session['loggedin'] = True
            session['role'] = "admin"
            return redirect(url_for('home'))
        else:
            flash('Такого пользователя не существует')
            return redirect(url_for('login'))

    return render_template("login.html", login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    regform = RegisterForm()

    if regform.validate_on_submit():
        habitant = dbase.get_habitant(regform.number_of_phone_regform.data)
        if habitant:
            flash('Такой пользователь уже существует')
        else:
            hashed_password = generate_password_hash(regform.password_regform.data)
            dbase.add_habitant(regform.number_of_phone_regform.data, regform.email_regform.data,
                               regform.fio_regform.data, hashed_password)
            return redirect(url_for('home'))
    return render_template("register.html", regform=regform)


@app.route('/request')
def request():
#     if session['role'] == "habitant":
#         # add_request_form = AddRequestForm()
#         # if add_request_form.submit.data:
    return render_template("request.html")


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('role', None)
    flash('Вы вышли из аккаунта')
    return redirect(url_for('home'))
