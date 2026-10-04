"""
    Database Configuration Module

    Description:
    - This module is responsible for database configuration and read values from environment file.

"""

# Importing Python packages
import environs

# Importing Flask packages

# Importing from project files


# --------------------------------------------------------------------------------------------------


# Creating env object
env = environs.Env()

env.read_env('.env')


# Reading values from environment file
DATABASE: str = env.str("DATABASE")
DB_HOST: str = env.str("DB_HOST")
DB_PORT: str = env.str("DB_PORT")
DB_USER: str = env.str("DB_USER")
DB_PASSWORD: str = env.str("DB_PASSWORD")
DB_NAME: str = env.str("DB_NAME")

DATABASE_URL: str = f"{DATABASE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


ADMIN_NAME: str = env.str("ADMIN_NAME")
ADMIN_CONTACT: str = env.str("ADMIN_CONTACT")
ADMIN_USERNAME: str = env.str("ADMIN_USERNAME")
ADMIN_EMAIL: str = env.str("ADMIN_EMAIL")
ADMIN_PASSWORD: str = env.str("ADMIN_PASSWORD")
