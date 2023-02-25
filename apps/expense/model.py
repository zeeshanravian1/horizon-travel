"""
    Expense Model

    Description:
    - This file contains model for expense table.

"""

# Importing Python packages
from sqlalchemy import (Float, ForeignKey, Integer)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class ExpenseTable(BaseTable):
    """
        Expense Table

        Description:
        - This table is used to create expense in database.

    """
    travel_detail_id: Mapped[int] = mapped_column(Integer, ForeignKey("traveldetail.id"),
                                                  nullable=False)
    price_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("pricecategory.id"),
                                                   nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
