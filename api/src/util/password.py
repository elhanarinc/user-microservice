import bcrypt


def encrypt(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def check(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))
