"""
    Role Pydantic Schemas

    Description:
    - This module contains all role schemas used by API.

"""

# Importing Python packages
from typing import (List)
from pydantic import (BaseModel, Field)

# Importing Flask packages

# Importing from project files
from apps import (BaseReadSchema, BasePaginationReadSchema)
from .configuration import (ROLE_ENUM, ID, ROLE, ROLE_DESCRIPTION)


# --------------------------------------------------------------------------------------------------


class RoleBaseSchema(BaseModel):
    """
        Role Base Schema

        Description:
        - This schema is used to validate role base data passed to API.

    """
    role_name: ROLE_ENUM | None = Field(None, example=ROLE)

    class Config:
        """
            Pydantic Config

            Description:
            - This class is used to configure Pydantic schema.

        """
        anystr_strip_whitespace = True
        orm_mode = True


class RoleCreateSchema(RoleBaseSchema):
    """
        Role create Schema

        Description:
        - This schema is used to validate role creation data passed to API.

    """
    role_name: ROLE_ENUM = Field(example=ROLE)


class RoleReadSchema(RoleCreateSchema, BaseReadSchema):
    """
        Role Read Schema

        Description:
        - This schema is used to validate role data returned from API.

    """


class RolePaginationReadSchema(BasePaginationReadSchema):
    """
        Role Pagination Read Schema

        Description:
        - This schema is used to validate role pagination data returned from API.

    """
    data: List[RoleReadSchema] = Field(example=[RoleReadSchema(id=1, role_name=ROLE)])


class RoleUpdateSchema(RoleCreateSchema):
    """
        Role Update Schema

        Description:
        - This schema is used to validate role update data passed to API.

    """


class RolePartialUpdateSchema(RoleBaseSchema):
    """
        Role Update Schema

        Description:
        - This schema is used to validate role update data passed to API.

    """
