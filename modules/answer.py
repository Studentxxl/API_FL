from flask import jsonify


def for_frontend(msg='', token='', code=405):
    """ Ответ фронтенду """
    answer = (jsonify(msg=msg, token=token), code, {'Content-Type': 'application/json; charset=utf-8'})
    return answer
