import datetime
import hashlib

from fastapi import Request

def device_hash(req: Request) -> str:
    ip = req.headers.get('X-Forwarded-For', req.client.host)
    ua = req.headers.get('User-Agent', '')
    return hashlib.sha256(f'{ip}{ua}'.encode()).hexdigest()


def string_epoch(date_str: str) -> int:
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        epoch = int(date_obj.timestamp())
        return epoch
    except ValueError:
        return 0
