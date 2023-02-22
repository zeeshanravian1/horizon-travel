"""
    Role Configuration Module

    Description:
    - This module is responsible for role configuration and read values from environment file.

"""

# Importing Python packages
from typing import (Literal)

# Importing Flask packages

# Importing from project files


# --------------------------------------------------------------------------------------------------


ROLE_ENUM = Literal["admin", "manager", "user"]

ROLE: str = "admin"
