from flask import current_app
from time import time
from pymysql import IntegrityError

from src.util.password import encrypt, check
from src.repo.user import insert as repo_insert, find_by_email as repo_find_by_email, \
    update_last_login_data as repo_update_last_login_data, update_password as repo_update_password, \
    list_users as repo_list_users, delete_user as repo_delete_user, update_user as repo_update_user
from src.errors.custom_error import CustomError
from src.util.jwt import encode


def register(user, repo=None):
    try:
        user.ts_registration = int(time())
        user.ts_last_login = int(time())
        user.password = encrypt(user.password)

        if repo is None:
            repo_insert(user)
        else:
            repo.insert(user)
    except IntegrityError as e:
        raise CustomError(
            message="Email or username has already been used.",
            status_code=400,
        )

    current_app.logger.debug("User with email %s registered" % user.email)

    return encode(user.jwt_payload(), current_app.config["JWT_SECRET"], current_app.config["JWT_TTL"])


def login(email, password, last_login_ip, repo=None):
    if repo is None:
        user = repo_find_by_email(email)
    else:
        user = repo.find_by_email(email)

    if user is None or not check(password, user.password):
        raise CustomError(
            message="Wrong mail or password.",
            status_code=401,
        )

    user.last_login_ip = last_login_ip

    if repo is None:
        repo_update_last_login_data(user, int(time()))
    else:
        repo.update_last_login_data(user, int(time()))

    current_app.logger.debug("User with email %s logged in" % user.email)

    return encode(user.jwt_payload(), current_app.config["JWT_SECRET"], current_app.config["JWT_TTL"])


def reset_password(email, new_password):
    user = repo_find_by_email(email)

    if user is None:
        raise CustomError(
            message="Operation is not allowed.",
            status_code=401,
        )

    repo_update_password(email, encrypt(new_password))

    current_app.logger.debug("Password updated for the user with email %s" % email)


def delete_account(email):
    user = repo_find_by_email(email)

    if user is None:
        raise CustomError(
            message="Operation is not allowed.",
            status_code=401,
        )

    repo_delete_user(email)

    current_app.logger.debug("User deleted with email %s" % email)


def list_users(name):
    users = repo_list_users(name)

    current_app.logger.debug("List users - search param: %s" % name)

    return users


def update_user(email, name=None, surname=None, age=None):
    user = repo_find_by_email(email)

    if user is None:
        raise CustomError(
            message="Operation is not allowed.",
            status_code=401,
        )

    current_app.logger.debug("User updated with email %s" % email)

    repo_update_user(email, name, surname, age)
