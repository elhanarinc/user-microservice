from flask import Blueprint, request, jsonify, g

from src.api.validator import validate, field
from src.service.user import login as service_login, register as service_register, \
    reset_password as service_reset_password, list_users as service_list_users, \
    delete_account as service_delete_account, update_user as service_update_user
from src.entity.user import User
from src.api.middleware import Middleware

bp = Blueprint("user", __name__)


@bp.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


@bp.route("/register", methods=['POST'])
def register():
    body = validate({
        "username": field("string", maxlength=180, required=True, empty=False, nullable=False),
        "email": field("email"),
        "password": field("password"),
        "name": field("string"),
        "surname": field("string"),
        "age": field("integer", min=15)
    }, request.get_json(force=True, silent=True))

    user = User(body)
    user.registration_ip = request.remote_addr
    user.last_login_ip = request.remote_addr

    token = service_register(user)

    return jsonify({"status": "OK", "token": token})


@bp.route("/login", methods=['POST'])
def login():
    body = validate({
        "email": field("email"),
        "password": field("password")
    }, request.get_json(force=True, silent=True))

    token = service_login(
        body["email"],
        body["password"],
        request.remote_addr
    )

    return jsonify({"status": "OK", "token": token})


@bp.route("/reset-password", methods=['POST'])
def reset_password():
    body = validate({
        "password": field("password")
    }, request.get_json(force=True, silent=True))

    token = request.headers.get("AUTHORIZATION")

    Middleware.auth(token)

    service_reset_password(g.user["email"], body["password"])

    return jsonify({"status": "OK", "message": "Password reset successful."})


@bp.route("/delete", methods=['DELETE'])
def delete_account():
    token = request.headers.get("AUTHORIZATION")

    Middleware.auth(token)

    service_delete_account(g.user["email"])
    return jsonify({"status": "OK", "message": "User has been deleted."})


@bp.route("/users", methods=['GET'])
def list_users():
    token = request.headers.get("AUTHORIZATION")
    Middleware.auth(token)

    name = request.args.get("search_param", type=str, default=None)

    users = service_list_users(name)

    return jsonify({"status": "OK", "data": users})


@bp.route("/update", methods=['PUT'])
def update_user():
    token = request.headers.get("AUTHORIZATION")
    Middleware.auth(token)

    body = validate({
        "name": field("string", required=True, empty=False, nullable=False),
        "surname": field("string", required=True, empty=False, nullable=False),
        "age": field("integer", min=15, required=True, empty=False, nullable=False)
    }, request.get_json(force=True, silent=True))

    service_update_user(g.user["email"], body.get("name", None), body.get("surname", None), body.get("age", None))

    return jsonify({"status": "OK", "message": "User has been updated."})
