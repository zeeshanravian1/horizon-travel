"""
    User Model

    Description:
    - This file contains model for user table.

"""

# Importing Python packages
from pydantic import (EmailStr)
from sqlalchemy import (Boolean, String)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class UserTable(BaseTable):
    """
        User Table

        Description:
        - This table is used to create users in database.

    """
    name: Mapped[str] = mapped_column(String(2_55), nullable=False)
    contact: Mapped[str] = mapped_column(String(2_55), nullable=False)
    username: Mapped[str] = mapped_column(String(2_55), unique=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(2_55), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(2_55), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password_otp: Mapped[str] = mapped_column(String(6), nullable=True, default=None)
    password_verified: Mapped[bool] = mapped_column(Boolean, nullable=True, default=None)
