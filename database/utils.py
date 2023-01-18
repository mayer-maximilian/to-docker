import os

def getenv(key, default_value):
    value = os.getenv(key, default_value)
    return value if value else default_value