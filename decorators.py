# Decorators
from flask import request

import utils


def log(action):
    def decorator_f(func):
        def wrapper_f(*args, **kwargs):
            token = request.args.get('token')
            device_id = utils.device_hash(request)
            start = request.args.get('start', '')
            retval = func(*args, **kwargs)
            print(f'{action}: {device_id if token is None else token} {start}')
            return retval
        return wrapper_f
    return decorator_f
