import hashlib

from flask import request


def device_hash(req: request) -> str:
    ip = req.headers.get('X-Forwarded-For', req.remote_addr)
    ua = req.headers.get('User-Agent', '')
    return hashlib.sha256(f'{ip}{ua}'.encode()).hexdigest()
