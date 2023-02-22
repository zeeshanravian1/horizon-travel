"""
    Database Initialization

    Description:
    - This module is responsible for initializing database.

"""

# Importing Python packages
from passlib.hash import (pbkdf2_sha256)

# Importing FastAPI packages

# Importing from project files
from apps.user.model import (UserTable)
from .configuration import (ADMIN_NAME, ADMIN_CONTACT, ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
from .session import (get_session)


# --------------------------------------------------------------------------------------------------


def insert_admin(session=get_session()):
    """
        Insert admin

        Description:
        - This function is used to insert admin.

        Parameters:
        - **None**

        Returns:
        - **None**

    """
    print("Calling insert_admin method")

    admin: UserTable = UserTable(
        name=ADMIN_NAME,
        contact=ADMIN_CONTACT,
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=pbkdf2_sha256.hash(ADMIN_PASSWORD),
        is_admin=True
    )

    session.add(admin)
    session.commit()
