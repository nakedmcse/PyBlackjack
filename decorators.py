# Decorators
from fastapi import Request
import utils


def log(action, request: Request):
    def decorator_f(func):
        def wrapper_f(*args, **kwargs):
            token = request.path_params.get('token')
            device_id = utils.device_hash(request)
            start = request.path_params.get('start', '')
            retval = func(*args, **kwargs)
            print(f'{action}: {device_id if token is None else token} {start}')
            return retval
        return wrapper_f
    return decorator_f
