"""
    Max Seats Model

    Description:
    - This file contains model for max seats table.

"""

# Importing Python packages
from sqlalchemy import (ForeignKey, Integer)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class MaxSeatsTable(BaseTable):
    """
        Max Seats Table

        Description:
        - This table is used to create max seats in database.

    """
    seats: Mapped[int] = mapped_column(Integer, nullable=False)

    travel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("traveltype.id"),
                                                unique=True, nullable=False)
