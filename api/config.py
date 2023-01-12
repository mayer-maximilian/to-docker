class Config:

    DEBUG = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://todo_user:todo_password@postgres_container/todo_db"  # when both front and backend run in docker containers
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://todo_user:todo_password@localhost:5432/todo_db"
