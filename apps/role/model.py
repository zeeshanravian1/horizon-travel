"""
    Role Model

    Description:
    - This file contains model for role table.

"""

# Importing Python packages
from sqlalchemy import (Enum)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database import (BaseTable, metadata)


# --------------------------------------------------------------------------------------------------


class RoleTable(BaseTable):
    """
        Role Table

        Description:
        - This table is used to create roles in database.

    """
    role_name: Mapped[str] = mapped_column(Enum("admin", "user", name="role_name_enum",
                                                metadata=metadata), unique=True, nullable=False)
