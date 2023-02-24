"""
    Price category Model

    Description:
    - This file contains model for price category table.

"""

# Importing Python packages
from sqlalchemy import (Float, String)
from sqlalchemy.orm import (Mapped, mapped_column)

# Importing Flask packages

# Importing from project files
from database.base import (BaseTable)


# --------------------------------------------------------------------------------------------------


class PriceCategoryTable(BaseTable):
    """
        Price Category Table

        Description:
        - This table is used to create price category in database.

    """
    name: Mapped[str] = mapped_column(String(2_55), unique=True, nullable=False)
