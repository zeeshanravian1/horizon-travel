"""
    Base Configuration Module

    Description:
    - This module is responsible for base configuration and read values from environment file.

"""

# Importing Python packages
from datetime import (datetime)

# Importing Flask packages

# Importing from project files


# --------------------------------------------------------------------------------------------------


ID: int = 1
CREATED_AT: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
UPDATED_AT: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

TOTAL: int = 0
PAGE: int = 1
LIMIT: int = 10
