import logging
from flask import Flask
from flask_cors import CORS

from src.errors.error_handlers import handle_custom_error
from src.errors.custom_error import CustomError
from src.api.middleware import Middleware
from src.api.resource.user import bp

app = Flask(__name__)
CORS(app)
app.wsgi_app = Middleware(app.wsgi_app)
app.register_error_handler(CustomError, handle_custom_error)

app.config.from_pyfile('config.py', silent=True)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()
