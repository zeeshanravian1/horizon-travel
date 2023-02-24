"""
    Travel Detail Model

    Description:
    - This file contains model for travel detail table.

"""

# Importing Python packages
from datetime import (datetime)
from sqlalchemy import (DateTime, Integer, ForeignKey)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class TravelDetailTable(BaseTable):
    """
        Travel Detail Table

        Description:
        - This table is used to create travel detail in database.

    """
    travel_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("travel_type.id"),
                                                nullable=False)
    departure_location_id: Mapped[int] = mapped_column(Integer, ForeignKey("location.id"),
                                                         nullable=False)
    departure_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    arrival_location_id: Mapped[int] = mapped_column(Integer, ForeignKey("location.id"),
                                                         nullable=False)
    arrival_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
