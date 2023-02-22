"""
    Base Model

    Description:
    - This file contains base model for all tables.

"""

# Importing Python packages
from datetime import (datetime)
from sqlalchemy import (func)
from sqlalchemy.orm import (Mapped, declared_attr, mapped_column)

# Importing Flask packages
from sqlalchemy_serializer import SerializerMixin

# Importing from project files
from .connection import (Base)


# --------------------------------------------------------------------------------------------------


class BaseTable(Base, SerializerMixin):
    """
        Base Table

        Description:
        - This is base model for all tables.

    """
    __abstract__ = True

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower().replace("table", "s")

    id: Mapped[int] = mapped_column(primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
