"""
    Travel Type Model

    Description:
    - This file contains model for travel type table.

"""

# Importing Python packages
from sqlalchemy import (String)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class TravelTypeTable(BaseTable):
    """
        Travel Type Table

        Description:
        - This table is used to create travel type in database.

    """
    name: Mapped[str] = mapped_column(String(2_55), unique=True, nullable=False)
