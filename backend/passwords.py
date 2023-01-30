from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    """
        Verify a password.

        :param plain_password: the plain, unhashed password
        :param hashed_password: the hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
        Hash a password.

        :param password: the plain, unhashed password
        :return: the hashed password
    """
    return pwd_context.hash(password)