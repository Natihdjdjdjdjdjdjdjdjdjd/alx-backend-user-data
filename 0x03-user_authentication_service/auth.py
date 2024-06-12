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

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers new user
        """
        try:
            self._db.find_user_by(email=email)
            # If a user already exist with the passed email
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        ha_pword = _hash_password(password)
        # Save the user to the database using self._db
        user = self._db.add_user(email, ha_pword)
        # Return the User object
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """the function that checks if a user's email and password are valid.
        """
        try:
            # Locate the user by email
            user_exit = self._db.find_user_by(email=email)
            if user_exit is not None:
                # Check if the password matches using bcrypt
                encod_password_bytes = password.encode('utf-8')
                hashed_password = user_exit.hashed_password
                if bcrypt.checkpw(encod_password_bytes, hashed_password):
                    return True
        except NoResultFound:
            return False
        return False
