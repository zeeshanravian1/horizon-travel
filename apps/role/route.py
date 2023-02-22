"""
    Role APIs Module

    Description:
    - This module is responsible for handling role APIs.
    - It is used to create, get, update, delete role details.

"""

# Importing Python packages
from sqlalchemy import (select, func)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (ROLE_NOT_FOUND)
from .model import (RoleTable)
from .schema import (RoleCreateSchema, RoleReadSchema,
                     RolePaginationReadSchema, RoleUpdateSchema)
from ..base import (CONTENT_TYPE)


role_router = Blueprint(
    name="Role",
    import_name=__name__,
    url_prefix="/role",
)


# --------------------------------------------------------------------------------------------------


@role_router.post("/")
def create_role(db_session: Session = get_session()):
    """
        Create a single role.

        Description:
        - This method is used to create a single role.

        Parameters:
        Role details to be created with following fields:
        - **role_name** (STR): Name of role. *--Required*
            - **Allowed values:** "admin", "manager", "user"

        Returns:
        Role details along with following information:
        - **id** (INT): Id of role.
        - **role_name** (STR): Name of role.
        - **created_at** (DATETIME): Datetime of role creation.
        - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling create_role method")

    try:
        record = RoleCreateSchema(**request.json)

        record = RoleTable(**record.dict())

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Role created successfully", "data": record.to_dict()},
                201, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Role already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid role id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single role route
@role_router.get("/<int:role_id>")
def get_role(
    role_id: int, db_session: Session = get_session()
) -> RoleReadSchema:
    """
        Get a single role.

        Description:
        - This method is used to get a single role.

        Parameters:
        - **role_id** (INT): Id of role. *--Required*

        Returns:
        Role details along with following information:
        - **id** (INT): Id of role.
        - **role_name** (STR): Name of role.
        - **created_at** (DATETIME): Datetime of role creation.
        - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling get_role method")

    query = select(RoleTable).where(RoleTable.id == role_id)

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": ROLE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "Role fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all roles route
@role_router.get("/")
def get_all_roles(
    page: int | None = 1, limit: int | None = 10,
    db_session: Session = get_session()
) -> RolePaginationReadSchema:
    """
        Get all roles.

        Description:
        - This method is used to get all roles.

        Parameters:
        - **None**

        Returns:
        Get all roles with following information:
        - **id** (INT): Id of role.
        - **role_name** (STR): Name of role.
        - **role_description** (STR): Description of role.
        - **created_at** (DATETIME): Datetime of role creation.
        - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling get_all_roles method")

    query = select(func.count(RoleTable.id))
    result = db_session.execute(query)
    total_count = result.scalar()

    print("total_count", total_count)

    if page and limit:
        query = select(RoleTable).where(
            RoleTable.id > (page - 1) * limit).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": ROLE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "Roles fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [role.to_dict() for role in result]}},
            200, CONTENT_TYPE)


# Update a single role route
@role_router.put("/<int:role_id>")
def update_role(
    role_id: int, db_session: Session = get_session()
) -> RoleReadSchema:
    """
        Update a single role.

        Description:
        - This method is used to update a single role by providing id.
        - If any field is not provided, it will be updated with null value.

        Parameters:
        - **role_id** (INT): ID of role to be updated. *--Required*
        Role details to be updated with following fields:
        - **role_name** (STR): Name of role. *--Required*
            - **Allowed values:** "admin", "manager", "user"

        Returns:
        Role details along with following information:
        - **id** (INT): Id of role.
        - **role_name** (STR): Name of role.
        - **created_at** (DATETIME): Datetime of role creation.
        - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling update_role method")

    try:
        record = RoleUpdateSchema(**request.json)

        query = select(RoleTable).where(RoleTable.id == role_id)

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": ROLE_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        result.role_name = record.role_name

        db_session.commit()

        return ({"success": True, "message": "Role updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Role already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid role id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single role route
@role_router.delete("/<int:role_id>")
def delete_role(
    role_id: int, db_session: Session = get_session()
) -> RoleReadSchema:
    """
        Delete a single role.

        Description:
        - This method is used to delete a single role by providing id.

        Parameters:
        - **role_id** (INT): ID of role to be deleted. *--Required*

        Returns:
        Role details along with following information:
        - **id** (INT): Id of role.
        - **role_name** (STR): Name of role.
        - **created_at** (DATETIME): Datetime of role creation.
        - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling delete_role method")

    query = select(RoleTable).where(RoleTable.id == role_id)

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": ROLE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    db_session.delete(result)
    db_session.commit()

    return ({"success": True, "message": "Role deleted successfully", "data": result.to_dict()},
            200, CONTENT_TYPE)
