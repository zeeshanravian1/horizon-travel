"""
    User Model

    Description:
    - This file contains model for user table.

"""

# Importing Python packages
from pydantic import (EmailStr)
from sqlalchemy import (Boolean, String, select)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages
from flask_login import (UserMixin)

# Importing from project files
from database.base import (BaseTable)
from database.session import (get_session)
from wsgi import (login_manager)


# --------------------------------------------------------------------------------------------------


@login_manager.user_loader
def load_user(id):
    """
        Load User

        Description:
        - This function is used to load user from database.

        Parameters:
        - id (int): User id.

        Returns:
        - UserTable: User table object.

    """
    with get_session() as session:
        return session.execute(select(UserTable).where(UserTable.id == id)).scalar_one_or_none()


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
