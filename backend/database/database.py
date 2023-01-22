from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from .utils import getenv

ENV = getenv('ENV', 'local')
POSTGRES_HOST = getenv('POSTGRES_HOST', 'todo-database-service')
POSTGRES_USERNAME = getenv('POSTGRES_USERNAME', 'local')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'local')

Base = declarative_base()

engine = create_engine(f"postgresql://{POSTGRES_USERNAME}:{quote_plus(POSTGRES_PASSWORD)}@"
                       f"{POSTGRES_HOST}/software-containerization{'?sslmode=require' if ENV != 'local' else ''}")

Session = sessionmaker(bind=engine)


def init_database():
    """ Initialize the database """
    Base.metadata.create_all(engine)
