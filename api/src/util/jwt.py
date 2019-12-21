import jwt
from time import time


def encode(payload, secret, ttl):
    payload["exp"] = int(time()) + (60 * ttl)
    return jwt.encode(payload, secret, algorithm='HS256').decode("utf-8")


def decode(encoded, secret):
    return jwt.decode(encoded, secret, algorithms=['HS256'])
