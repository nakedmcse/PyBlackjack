import datetime
import hashlib

from flask import request


def device_hash(req: request) -> str:
    ip = req.headers.get('X-Forwarded-For', req.remote_addr)
    ua = req.headers.get('User-Agent', '')
    return hashlib.sha256(f'{ip}{ua}'.encode()).hexdigest()


def string_epoch(date_str: str) -> int:
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        epoch = int(date_obj.timestamp())
        return epoch
    except ValueError:
        return 0
