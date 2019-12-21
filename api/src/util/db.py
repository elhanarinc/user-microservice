import pymysql
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            db=current_app.config["MYSQL_DB"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            passwd=current_app.config["MYSQL_PASSWORD"],
            charset=current_app.config["MYSQL_CHARSET"],
            autocommit=True
        )
        g.cursor = g.db.cursor(pymysql.cursors.DictCursor)

        current_app.logger.debug("Db connection opened.")


def close_db():
    db = g.pop('db', None)
    cursor = g.pop('cursor', None)

    if cursor is not None:
        cursor.close()

    if db is not None:
        db.close()

    current_app.logger.debug("Db connection closed.")
