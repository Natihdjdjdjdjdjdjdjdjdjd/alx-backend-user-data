#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Creates new User
        """
        session = self._session
        try:
            first_user = User(email=email, hashed_password=hashed_password)
            session.add(first_user)
            session.commit()
        except Exception:
            session.rollback()
            first_user = None
        return first_user

    def find_user_by(self, **kwargs) -> User:
        """ Find user by a given attribute
            Args:
                - Dictionary of attributes to use as search
                  parameters
            Return:
                - User object
        """

        attrs, vals = [], []
        for attr, val in kwargs.items():
            if not hasattr(User, attr):
                raise InvalidRequestError()
            attrs.append(getattr(User, attr))
            vals.append(val)

        session = self._session
        query = session.query(User)
        user = query.filter(tuple_(*attrs).in_([tuple(vals)])).first()
        if not user:
            raise NoResultFound()
        return user
