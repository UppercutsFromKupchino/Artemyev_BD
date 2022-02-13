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

    def get_all_flats(self, id_habitant):
        try:
            self.__cursor.execute(f"""SELECT number_of_flat FROM habitant_flat WHERE id_of_habitant='{id_habitant}'""")
            buildings = self.__cursor.fetchall()
            return buildings
        except psycopg2.errors:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def add_request(self, habitant, flat, date, text):
        try:
            self.__cursor.execute(f"""INSERT INTO request(id_of_habitant,number_of_flat,datetime_of_request,
                                      text_of_request,id_of_status)
                                      VALUES('{habitant}','{flat}','{date}','{text}','1')""")
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

    def get_requests_habitant(self, id_habitant):
        try:
            self.__cursor.execute(f"""SELECT DISTINCT request.number_of_flat,request.datetime_of_request,
                                request.text_of_request,status.name_of_status FROM request
                                JOIN status ON request.id_of_status = status.id_of_status
                                JOIN habitant_flat ON request.number_of_flat=habitant_flat.number_of_flat
                                WHERE request.id_of_habitant = '{id_habitant}'""")
            requests = self.__cursor.fetchall()
            return requests
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_requests_worker(self, id_worker):
        try:
            self.__cursor.execute(f"""SELECT DISTINCT request.number_of_flat,request.datetime_of_request,
                                request.text_of_request,request.id_of_request,status.name_of_status FROM request
                                JOIN executor ON request.id_of_request=executor.id_of_request
                                JOIN status ON request.id_of_status=status.id_of_status
                                WHERE executor.id_of_worker = '{id_worker}'""")
            requests = self.__cursor.fetchall()
            return requests
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_all_statuses(self):
        try:
            self.__cursor.execute(f"""SELECT * FROM role_of_user""")
            roles = self.__cursor.fetchall()
            return roles
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_workers_admin(self):
        try:
            self.__cursor.execute(f"""SELECT worker.id_of_worker,_user.fio_of_user FROM worker
            JOIN _user ON worker.id_of_worker=_user.id_of_user""")
            requests = self.__cursor.fetchall()
            return requests
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_requests_admin(self):
        try:
            self.__cursor.execute(f"""SELECT request.number_of_flat,request.datetime_of_request,
                                       request.text_of_request,request.id_of_request FROM request
                                       LEFT OUTER JOIN executor ON request.id_of_request=executor.id_of_request
                                       WHERE executor.id_of_worker is null""")
            requests = self.__cursor.fetchall()
            return requests
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_list_of_workers(self):
        try:
            self.__cursor.execute("""SELECT _user.fio_of_user,profession.name_of_profession FROM _user
                                     JOIN worker ON _user.id_of_user=worker.id_of_worker
                                     JOIN profession ON worker.id_of_profession=profession.id_of_profession""")
            list_of_workers = self.__cursor.fetchall()
            return list_of_workers
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def execute_request_admin(self, id_worker, id_request):
        # try:
            self.__cursor.execute(f"""INSERT INTO executor VALUES('{id_worker}','{id_request}')""")
            self.__cursor.execute(f"""UPDATE request SET id_of_status='2' WHERE id_of_request='{id_request}'""")
            self.__db.commit()
        # except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('request'))

    def get_list_of_professions(self):
        try:
            self.__cursor.execute(f"""SELECT id_of_profession,name_of_profession FROM profession""")
            professions = self.__cursor.fetchall()
            return professions
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('admin'))

    def get_list_of_all_workers(self):
        try:
            self.__cursor.execute("""SELECT id_of_user, fio_of_user FROM _user WHERE id_of_role = '2'""")
            all_workers = self.__cursor.fetchall()
            return all_workers
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('admin'))

    def add_profession_for_a_worker(self, id_profession, id_worker):
        try:
            self.__cursor.execute(f"""INSERT INTO worker VALUES ('{id_worker}','{id_profession}')""")
            self.__db.commit()
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('admin'))

    def get_list_of_flats(self):
        try:
            self.__cursor.execute("""SELECT number_of_flat FROM flat""")
            flats = self.__cursor.fetchall()
            return flats
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('admin_flat'))

    def get_list_of_all_habitants(self):
        try:
            self.__cursor.execute("""SELECT id_of_user,fio_of_user FROM _user JOIN habitant
                                  ON _user.id_of_user=habitant.id_of_habitant""")
            all_habitants = self.__cursor.fetchall()
            return all_habitants
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('admin_flat'))

    def add_flat_to_habitant(self, flat, habitant):
        try:
            self.__cursor.execute(f"""INSERT INTO habitant_flat VALUES('{habitant}','{flat}')""")
            self.__db.commit()
            flash('Пользователь добавлен успешно')
        except:
            flash('Ошибка взаимодействия с базой данных, попробуйте позже')
            return redirect(url_for('admin_flat'))
