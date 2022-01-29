import psycopg2
import psycopg2.errors
import psycopg2.extras
from flask import redirect, url_for, flash


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_user(self, phone):
        try:
            self.__cursor.execute(f"""SELECT * FROM _user WHERE number_of_users_phone ='{phone}' """)
            user = self.__cursor.fetchone()
            # self.conn.close()
            return user
        except psycopg2.errors as e:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('login'))

    def get_worker(self, phone):
        try:
            self.__cursor.execute(f"""SELECT * FROM worker WHERE number_of_users_phone = '{phone}'""")
            worker = self.__cursor.fetchone()
            return worker
        except psycopg2.errors as e:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('index'))

    def get_admin(self, login):
        try:
            self.__cursor.execute(f"""SELECT * FROM administrator WHERE login_of_admin = '{login}'""")
            admin = self.__cursor.fetchone()
            return admin
        except psycopg2.errors as e:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('login'))

    def get_habitant(self, phone):
        try:
            self.__cursor.execute(f"""SELECT * FROM habitant WHERE number_of_users_phone = '{phone}'""")
            habitant = self.__cursor.fetchone()
            return habitant
        except psycopg2.errors as e:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('register'))

    def add_habitant(self, phone, email, fio, password):
        try:
            self.__cursor.execute(f"""INSERT INTO _user VALUES('{phone}','{email}','{fio}','{password}')""")
            self.__db.commit()
            self.__cursor.execute(f"""INSERT INTO habitant(number_of_users_phone,id_of_role)
                                    VALUES('{phone}','1')""")
            self.__db.commit()
        except psycopg2.errors as e:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('register'))
