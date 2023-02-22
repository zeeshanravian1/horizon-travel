"""
    Base Read Pydantic Schema

    Description:
    - This module contains base read schema used by API.

"""

# Importing Python packages
from datetime import (datetime)
from typing import (List)
from pydantic import (BaseModel, Field)

# Importing Flask packages

# Importing from project files
from .configuration import (ID, CREATED_AT, UPDATED_AT, TOTAL, PAGE, LIMIT)


# --------------------------------------------------------------------------------------------------


class BaseReadSchema(BaseModel):
    """
        Base Read Schema

        Description:
        - This schema is used to validate base data returned from API.

    """
    id: int = Field(example=ID)
    created_at: datetime | None = Field(None, example=CREATED_AT)
    updated_at: datetime | None = Field(None, example=UPDATED_AT)


class BasePaginationReadSchema(BaseModel):
    """
        Base Pagination Read Schema

        Description:
        - This schema is used to validate base pagination data returned from API.

    """
    total: int = Field(example=TOTAL)
    page: int = Field(example=PAGE)
    limit: int = Field(example=LIMIT)
    data: List = Field(example=[])
