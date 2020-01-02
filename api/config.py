import os

class Config():
    """ Flask configuration. """
    ORATOR_DATABASES = {
        "default": os.getenv("ORATOR_DATABASE", "local"),
        "local": {
            "driver": "sqlite",
            "database": f"{os.getcwd()}/api.db"
        },
        "dev": {
            "driver": "postgres",
            "host": os.getenv("DATABASE_HOST"),
            "database": os.getenv("DATABASE_DATABASE"),
            "user": os.getenv("DATABASE_USER"),
            "password": os.getenv("DATABASE_PASSWORD"),
        }
    }
    JWT_SECRET_KEY = "super_secret_key"
