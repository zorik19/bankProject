import datetime
import hashlib
import json
from typing import Union


def serializer(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def hash_payload(payload: Union[bytes, dict]) -> str:
    """
    makes md5 hash from bytes object like raw json or dict
    :param payload: dict o raw_bytes
    :return: hashed name
    """
    if isinstance(payload, dict):
        payload = str(payload).encode('utf-8')
        # todo: do we need use json?
        # json.dumps(payload, default=serializer)
    name = hashlib.md5()

    name.update(payload)
    return name.hexdigest()
