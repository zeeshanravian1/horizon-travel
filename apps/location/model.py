"""
    Location Model

    Description:
    - This file contains model for location table.

"""

# Importing Python packages
from sqlalchemy import (Float, String)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class LocationTable(BaseTable):
    """
        Location Table

        Description:
        - This table is used to create location in database.

    """
    name: Mapped[str] = mapped_column(String(2_55), unique=True, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
