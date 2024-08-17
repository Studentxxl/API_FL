import hashlib
from secret import salt


def hash_password(pwd):
    """ Солит, хеширует строку пароля"""
    salted_password = pwd.encode() + salt.CONST_SALT.encode()
    result = hashlib.sha256(salted_password).hexdigest()
    return result
