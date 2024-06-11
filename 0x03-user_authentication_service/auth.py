#!/usr/bin/env python3
"""
a module that interact an authentication module
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound

def _hash_password(password: str) -> bytes:
    """ let creates password hash
    """
    encod_pwd = password.encode()
    return bcrypt.hashpw(encod_pwd, bcrypt.gensalt())
