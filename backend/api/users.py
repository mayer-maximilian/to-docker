from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api import auth_required
from api.swagger_models import AddUserSchema, UpdateUserSchema
from database import Session
from database.users import list_users, change_password, add_user, find_db_user, disable_user, delete_user
from passwords import get_password_hash


router = APIRouter()


@router.post('/register', status_code=202)
def register(user: AddUserSchema):
    """Add a user to the database"""
    with Session() as session:
        add_user(
            session,
            username=user.username,
            hashed_password=get_password_hash(user.password),
            disabled=user.disabled
        )


@router.get('/get-users', dependencies=[Depends(auth_required)], status_code=200)
def get_users():
    """Get all the users, no matter whether they are active or not"""
    with Session() as session:
        users = list_users(session)
        for user in users:
            user.pop('hashed_password')
    return {'users': users}


@router.post('/change-password', dependencies=[Depends(auth_required)], status_code=202)
def change_password_api(form_data: OAuth2PasswordRequestForm = Depends()):
    """Change password for a user"""
    with Session() as session:
        change_password(session, form_data.username, form_data.password)
    return {'message': 'Password changed'}


@router.post('/add-user', dependencies=[Depends(auth_required)], status_code=202)
def post_user(user: AddUserSchema):
    """Add a user to the database"""
    with Session() as session:
        add_user(
            session,
            username=user.username,
            hashed_password=get_password_hash(user.password),
            disabled=user.disabled
        )


@router.post('/delete-user', dependencies=[Depends(auth_required)], status_code=202)
def del_user(username):
    """Delete a user from the database"""
    with Session() as session:
        delete_user(session, username)


@router.post('/update-user', dependencies=[Depends(auth_required)], status_code=202)
def update_user(user: UpdateUserSchema):
    """Update a user that is in the database"""
    with Session() as session:
        db_user = find_db_user(session, user.username)
        db_user.disabled=user.disabled
        session.commit()


@router.post('/enable-user', dependencies=[Depends(auth_required)], status_code=202)
def enable_user(username):
    """Set a user to active"""
    with Session() as session:
        disable_user(session, username, False)


@router.post('/disable-user', dependencies=[Depends(auth_required)], status_code=202)
def disable_user(username):
    """Set a user to disabled"""
    with Session() as session:
        disable_user(session, username, True)
