from fastapi import HTTPException
from sqlalchemy import Column, String, Integer, Boolean

from database.database import Base


class UserNotFoundException(HTTPException):
    """The exception that is thrown when the give user doesn't exist"""
    def __init__(self, message='User not found'):
        super().__init__(status_code=404, detail=message)


class User(Base):
    """ORM class for the users"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), index=True, unique=True)
    hashed_password = Column(String(64), nullable=False)
    disabled = Column(Boolean, default=False)


def add_user(session, username, hashed_password, disabled=False):
    """
        Add a user to the database or update one if it already exists

        :param session: A session object to interact with the database
        :param username: The username of the user which is used to log in with
        :param hashed_password: The hashed password of the user
        :param disabled: Optional flag to control whether the user is active or not
        :return: A message whether the user was updated or created
    """
    user = find_user(session, username)
    if user:
        user = User(**{k: v for k, v in user.items() if k in User.__mapper__.attrs.keys()})
        user.username = username
        user.hashed_password = hashed_password
        user.disabled = disabled
        msg = 'User Updated'
    else:
        user = User(username=username, hashed_password=hashed_password, disabled=disabled)
        msg = 'User created'
    session.add(user)
    session.commit()
    return msg


def list_users(session):
    """
        List all users in the database

        :param session: A session object to interact with the database
        :return: A list containing all users
    """
    users = session.query(User).all()
    return [user.__dict__ for user in users]


def find_user(session, username):
    """
        Find a user by the username

        :param session: A session object to interact with the database
        :param username: The username of the user that should be found
        :return: A user, or None if the user doesn't exist
    """
    user = session.query(User).filter(User.username==username).one_or_none()
    return user.__dict__ if user else None


def delete_user(session, username):
    """
        Delete a user by their username

        :param session: A session object to interact with the database
        :param username: The name of the user to be deleted
    """
    user = session.query(User).filter(User.username==username).one_or_none()
    if not user:
        raise UserNotFoundException
    session.delete(user)
    session.commit()


def disable_user(session, username, disabled):
    """
        Disable a user or set it to active

        :param session: A session object to interact with the database
        :param username: The username of the user to disable or activate
        :param disabled: A boolean whether the user should be disabled or not
    """
    user = session.query(User).filter(User.username == username).one_or_none()
    user.disabled = disabled
    session.commit()
