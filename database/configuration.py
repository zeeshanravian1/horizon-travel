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


# Reading values from environment file
DATABASE: str = env.str("DATABASE")
DB_HOST: str = env.str("DB_HOST")
DB_PORT: str = env.str("DB_PORT")
DB_USER: str = env.str("DB_USER")
DB_PASSWORD: str = env.str("DB_PASSWORD")
DB_NAME: str = env.str("DB_NAME")

DATABASE_URL: str = f"{DATABASE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
