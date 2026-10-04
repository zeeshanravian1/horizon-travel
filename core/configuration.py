"""
    Core Configuration Module

    Description:
    - This module is responsible for core configuration and read values from environment file.

"""

# Importing Python packages
import environs

# Importing Flask packages

# Importing from project files


# --------------------------------------------------------------------------------------------------


# Creating env object
env = environs.Env()


CORS_ALLOW_ORIGINS: str = env.str("CORS_ALLOW_ORIGINS")
CORS_ALLOW_METHODS: str = env.str("CORS_ALLOW_METHODS")
CORS_ALLOW_HEADERS: str = env.str("CORS_ALLOW_HEADERS")

PROJECT_TITLE: str = "Horizon Travels"
PROJECT_DESCRIPTION: str = "Horizon Travels Documentation"

VERSION: str = "1.0.0"
API_PREFIX: str = "/api/v1"
