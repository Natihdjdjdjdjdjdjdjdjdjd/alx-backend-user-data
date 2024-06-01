#!/usr/bin/env python3
"""
module that encript encrypting passwords
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    perform the hashing Salted that pass  pass generation
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ the functini that check if password is valid?
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
