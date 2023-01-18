import re
import secrets
import string
from passlib.context import CryptContext

from database import Session
from database.users import add_user, find_user

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def is_password_valid(password: string):
    """
        Check is given password is valid;
        - Minimal 20 characters long
        - At least 1 uppercase a-z
        - At least 1 lowercase a-z
        - At least 1 numeric character
        - At least 1 special character

        :param: the password to check
        :return: object or None
    """
    reg = "^(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[" + string.punctuation + "]).*$"
    pat = re.compile(reg)
    mat = re.search(pat, password)
    return mat


def generate_password(generated_pw_length: int):
    """
        Generate strong password using letters, numbers and special characters.

        :param: requested password length
        :return: generated password
    """
    pw_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(pw_chars) for _ in range(generated_pw_length))
    return password


def set_user():
    """
        Ask user for input to create a new, or update an user with API access.
        The user is saved in the MongoDB 'auth' collection and has direct access
        to the secure API endpoints.

        :return: dictionary with userdata
    """
    with Session() as session:
        print('Please provide the user data')
        username = input('Username: ')
        overwrite = 'n'

        while find_user(session, username) is not None and overwrite.lower() == 'n':
            overwrite = input('Username exists, would you like to override? [y/n]: ')
            if overwrite.lower() == 'n':
                username = input('Enter another username: ')

        return {'username': username}

def set_password():
    """
        Ask for a (new) password for the user. The password is checked against
        basic rules and returned in hashed format.

        :return: hash of password
    """
    password = input('Password: ')

    if password and password.strip():
        if not is_password_valid(password):
            print('Password needs to be at least 20 characters and contain a lowercase, uppercase and special '
                  'character. Please try again or leave empty to generate a password.')
            set_password()

        password_check = input('Password (again): ')

        if password != password_check:
            print('Passwords do not match, please try again')
            set_password()
    else:
        # Nothing entered. Generate password
        password = generate_password(20)
        while not is_password_valid(password):
            password = generate_password(20)

        print(f"No password given. Generated password:\n{password}\n"
              f"Please store the password somewhere safe. You won't be able to retrieve it later.")

    return pwd_context.hash(password)


if __name__ == '__main__':
    with Session() as session:
        user = set_user()
        user['hashed_password'] = set_password()
        add_user(session, **user)
        print('User created!')
