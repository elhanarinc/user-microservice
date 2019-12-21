from flask import g

from src.entity.user import User
from src.util.db import get_db, close_db


def insert(user):
    get_db()

    sql = "INSERT INTO user (username, email, password, name, surname, age, ts_registration, ts_last_login, last_login_ip, registration_ip)"
    sql = "{} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(sql)

    args = (
        user.username, user.email, user.password, user.name, user.surname, user.age, user.ts_registration,
        user.ts_last_login, user.last_login_ip, user.registration_ip
    )

    g.cursor.execute(sql, args)

    close_db()


def find_by_email(email):
    get_db()

    g.cursor.execute("SELECT * FROM user WHERE email = %s", [email])
    row = g.cursor.fetchone()

    close_db()

    if row is None:
        return None

    return User(row)


def find_by_id(user_id):
    get_db()

    g.cursor.execute("SELECT * FROM user WHERE id = %s", [user_id])
    row = g.cursor.fetchone()

    close_db()

    if row is None:
        return None

    return User(row)


def update_last_login_data(user, ts_now):
    get_db()

    args = (ts_now, user.last_login_ip, user.id)

    g.cursor.execute("UPDATE user SET ts_last_login = %s, last_login_ip = %s WHERE id = %s", args)

    close_db()


def update_password(email, password):
    get_db()

    args = (password, email)

    g.cursor.execute("UPDATE user SET password = %s WHERE email = %s", args)

    close_db()


def delete_user(email):
    get_db()

    g.cursor.execute("DELETE FROM user WHERE email = %s", email)

    close_db()


def list_users(name):
    where_statements = None

    if name is not None:
        sql_name = "'%" + name + "%'"
        where_statements = " WHERE username LIKE %s OR email LIKE %s" % (sql_name, sql_name)

    sql = "SELECT username, email, name, surname, age FROM user"
    if where_statements is not None:
        sql += where_statements

    get_db()

    g.cursor.execute(sql)
    rows = g.cursor.fetchall()

    close_db()

    return rows


def update_user(email, name, surname, age):
    get_db()

    args = (name, surname, age, email)

    sql = "UPDATE user SET name = %s, surname = %s, age = %s WHERE email = %s"

    g.cursor.execute(sql, args)

    close_db()
