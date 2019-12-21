from flask import jsonify, Response


def handle_custom_error(error):
    response: Response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
