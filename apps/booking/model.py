"""
    Booking Model

    Description:
    - This file contains model for booking table.

"""

# Importing Python packages
from sqlalchemy import (Enum, Float, ForeignKey, Integer)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class BookingTable(BaseTable):
    """
        Booking Table

        Description:
        - This table is used to create booking in database.

    """
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True,
                                        default=None)
    travel_detail_id: Mapped[int] = mapped_column(Integer, ForeignKey("traveldetail.id"),
                                                  nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(Enum("success", "cancelled", name="booking_status"),
                                        nullable=False, default="success")
    refund_amount: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
