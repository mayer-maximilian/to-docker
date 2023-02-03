from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from .utils import getenv

# POSTGRES_HOST = getenv('POSTGRES_SERVICE_SERVICE_HOST', 'localhost')
POSTGRES_HOST = getenv('POSTGRES_HOST', 'localhost')
POSTGRES_USERNAME = getenv('POSTGRES_USERNAME', 'local').strip()
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD', 'local').strip()

Base = declarative_base()

print(f"postgresql://{POSTGRES_USERNAME}:{quote_plus(POSTGRES_PASSWORD)}@"
      f"{POSTGRES_HOST}/software-containerization")

engine = create_engine(f"postgresql://{POSTGRES_USERNAME}:{quote_plus(POSTGRES_PASSWORD)}@"
                       f"{POSTGRES_HOST}/software-containerization")

Session = sessionmaker(bind=engine)


def init_database():
    """ Initialize the database """
    Base.metadata.create_all(engine)
