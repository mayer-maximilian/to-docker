class Config:

    DEBUG = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://testusr:password@postgres/testdb"
