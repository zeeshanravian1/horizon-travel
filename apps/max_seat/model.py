"""
    Max Seat Model

    Description:
    - This file contains model for max seat table.

"""

# Importing Python packages
from sqlalchemy import (ForeignKey, Integer)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class MaxSeatTable(BaseTable):
    """
        Max Seat Table

        Description:
        - This table is used to create max seat in database.

    """
    seats: Mapped[int] = mapped_column(Integer, nullable=False)

    travel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("traveltype.id"),
                                                unique=True, nullable=False)
