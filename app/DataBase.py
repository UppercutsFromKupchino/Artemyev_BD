import psycopg2
import psycopg2.errors
import psycopg2.extras
from flask import redirect, url_for, flash, session


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = self.__db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_user(self, phone, role):
        try:
            self.__cursor.execute(f"""SELECT * FROM _user WHERE number_of_users_phone ='{phone}' AND
                                  id_of_role = '{role}'""")
            user = self.__cursor.fetchone()
            return user

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('login'))

    def add_user(self, phone, email, fio, password, role):
        try:
            self.__cursor.execute(f"""INSERT INTO _user VALUES('{phone}','{email}','{fio}','{password}','{role}')""")
            self.__db.commit()
            flash('Пользователь успешно добавлен')

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('register'))

    def add_habitant(self, users_id):
        try:
            self.__cursor.execute(f"""INSERT INTO habitant(id_of_habitant) VALUES('{users_id}')""")
            self.__db.commit()
            flash('Житель успешно добавлен')

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('register'))

    # def add_worker(self):
    #     try:
    #         self.__cursor.execute(f"""INSERT INTO worker(id_of_worker, id_of_profession) VALUES()""")

    def get_all_buildings(self, id_habitant):
        try:
            self.__cursor.execute(f"""SELECT DISTINCT number_of_building FROM habitant_flat JOIN flat on
                                      habitant_flat.id_of_flat=flat.id_of_flat
                                      WHERE id_of_habitant = '{id_habitant}'""")
            buildings = self.__cursor.fetchall()
            buildings_list = []
            buildings_len = len(buildings)
            for i in range(buildings_len):
                buildings_list.append(buildings[i][0])
            buildings = buildings_list
            return buildings

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_all_flats(self, id_habitant):
        try:
            self.__cursor.execute(f"""SELECT DISTINCT number_of_flat FROM habitant_flat JOIN flat on
                                      habitant_flat.id_of_flat=flat.id_of_flat
                                      WHERE id_of_habitant = '{id_habitant}'""")
            flats = self.__cursor.fetchall()
            flats_list = []
            flats_len = len(flats)
            for i in range(flats_len):
                flats_list.append(flats[i][0])
            flats = flats_list
            return flats

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_id_of_flat(self, building, flat):
        try:
            self.__cursor.execute(f"""SELECT id_of_flat FROM flat WHERE number_of_building = '{building}'
                                      AND number_of_flat = '{flat}'""")
            id_of_flat = self.__cursor.fetchone()
            return id_of_flat

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def add_request(self, habitant, flat, date, text):
        try:
            self.__cursor.execute(f"""INSERT INTO request(id_of_habitant,id_of_flat,datetime_of_request,text_of_request,
                                      id_of_status) VALUES('{habitant}','{flat}','{date}','{text}','1')""")
            self.__db.commit()

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_roles(self):
        try:
            self.__cursor.execute(f"""SELECT * FROM role_of_user""")
            roles = self.__cursor.fetchall()
            return roles

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('register'))

    def get_users_id(self, phone, role):
        try:
            self.__cursor.execute(f"""SELECT id_of_user FROM _user WHERE number_of_users_phone = '{phone}' AND
                                  id_of_role = '{role}'""")
            users_id = self.__cursor.fetchone()
            return users_id

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('register'))

    def get_users_password_on_login(self, phone):
        try:
            self.__cursor.execute(f"""SELECT id_of_user,password_of_user,id_of_role FROM _user
                                  WHERE number_of_users_phone = '{phone}'""")
            users = self.__cursor.fetchall()
            return users

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('login'))

    def get_users_roles_on_login(self, phone):
        try:
            self.__cursor.execute(f"""SELECT role_of_user.id_of_role, role_of_user.name_of_role FROM role_of_user
                                  JOIN _user ON _user.id_of_role = role_of_user.id_of_role
                                  WHERE _user.number_of_users_phone = '{phone}'""")

            users_roles = self.__cursor.fetchall()
            return users_roles

        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('login'))

    def get_user_on_role_and_phone(self, phone, role):
        try:
            self.__cursor.execute(f"""SELECT id_of_user, password_of_user, id_of_role FROM _user
                                  WHERE number_of_users_phone = '{phone}' AND id_of_role = '{role}'""")
            user = self.__cursor.fetchone()
            return user
        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('login'))
