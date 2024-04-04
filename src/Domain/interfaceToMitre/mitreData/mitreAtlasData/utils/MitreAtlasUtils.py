import hashlib
import uuid


def get_uuid_from_string(str_id: str):
    str_hex = hashlib.md5(str_id.encode("UTF-8")).hexdigest()
    return uuid.UUID(hex=str_hex, version=4)