from app import app
from flask import render_template, redirect, url_for, flash, g, session
from app.DataBase import DataBase
from app.forms import LoginForm, RegisterForm, AddRequestForm, LoginMoreThanOneForm, ChangeStatusOfRequestWorker
from app.forms import ExecuteRequestForWorker, SelectProfessionForAWorker
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2
import psycopg2.errors
import datetime


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    dbname = "dbtfg5sbci8onm"
    user = "krfwfcoixkstbw"
    password = "d0a601c99b33a3b98b76325d982a5aa0f7f563bf4c7d66a26e8819578b470d2d"
    host = "ec2-54-220-243-77.eu-west-1.compute.amazonaws.com"
    conn = psycopg2.connect(dbname, user, password, host=host)
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
    if 'loggedin' in session:

        if session['id_of_role'] == 1:
            add_request_form = AddRequestForm()

            flats = dbase.get_all_flats(session['id_of_user'])
            flats_len = len(flats)
            for i in range(flats_len):
                add_request_form.number_of_flat.choices.append(flats[i][0])

            requests = dbase.get_requests_habitant(session['id_of_user'])
            requests_len = len(requests)

            if add_request_form.validate_on_submit():

                id_of_habitant = session['id_of_user']

                current_datetime = datetime.datetime.now()

                dbase.add_request(id_of_habitant,
                                  add_request_form.number_of_flat.data,
                                  current_datetime,
                                  add_request_form.text_of_request.data)

            return render_template("request.html", add_request_form=add_request_form, requests=requests,
                                   requests_len=requests_len)

        elif session['id_of_role'] == 2:

            change_status_of_request_worker = ChangeStatusOfRequestWorker()

            requests_worker = dbase.get_requests_worker(session['id_of_user'])
            requests_len = len(requests_worker)

            change_status_of_request_worker.select_status.choices = dbase.get_all_statuses()

            return render_template("request.html", requests_worker=requests_worker, requests_len=requests_len,
                                   change_status_of_request_worker=change_status_of_request_worker)

        elif session['id_of_role'] == 3:

            execute_request_for_worker = ExecuteRequestForWorker()
            workers = dbase.get_workers_admin()
            print(workers)

            requests = dbase.get_requests_admin()
            requests_len = len(requests)
            execute_request_for_worker.select_executor.choices = workers

            list_of_workers = dbase.get_list_of_workers()
            list_of_workers_len = len(list_of_workers)

            if execute_request_for_worker.changing_submit.data:

                dbase.execute_request_admin(execute_request_for_worker.select_executor.data,
                                            execute_request_for_worker.hidden_id_of_request.data)

                return redirect(url_for('request'))

            return render_template("request.html", execute_request_for_worker=execute_request_for_worker,
                                   requests_len=requests_len, requests=requests, list_of_workers=list_of_workers,
                                   list_of_workers_len=list_of_workers_len)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'loggedin' in session:
        if session['id_of_role'] == 3:

            select_profession_for_a_worker = SelectProfessionForAWorker()

            select_profession_for_a_worker.select_profession.choices = dbase.get_list_of_professions()
            select_profession_for_a_worker.select_worker.choices = dbase.get_list_of_all_workers()

            if select_profession_for_a_worker.submit.data:

                dbase.add_profession_for_a_worker(select_profession_for_a_worker.select_profession.data,
                                                  select_profession_for_a_worker.select_worker.data)
                return redirect(url_for('admin'))

            return render_template("admin.html", select_profession_for_a_worker=select_profession_for_a_worker)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('role', None)
    session.clear()
    flash('Вы вышли из аккаунта')
    return redirect(url_for('home'))
