"""
    User APIs Module

    Description:
    - This module is responsible for handling user APIs.
    - It is used to create, get, update, delete user details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (USER_NOT_FOUND)
from .model import (UserTable)
from ..base import (CONTENT_TYPE)


user_router = Blueprint(
    name="UserRouter",
    import_name=__name__,
    url_prefix="/user",
)


# --------------------------------------------------------------------------------------------------


# Get a single user route
@user_router.get("/<int:user_id>/")
def get_user(
    user_id: int, db_session: Session = get_session()
):
    """
        Get a single user.

        Description:
        - This method is used to get a single user.

        Parameters:
        - **user_id** (INT): Id of user. *--Required*

        Returns:
        user details along with following information:
        - **id** (INT): Id of user.
        - **name** (STR): Name of user.
        - **contact** (STR): Contact of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **password** (STR): Password of user.
        - **is_admin** (BOOL): Is user admin or not.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling get_user method")

    query = select(UserTable).where(and_(UserTable.id == user_id,
                                         UserTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "user fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all users route
@user_router.get("/")
def get_all_users(
    page: int | None = 1, limit: int | None = 10,
    db_session: Session = get_session()
):
    """
        Get all users.

        Description:
        - This method is used to get all users.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all users with following information:
        - **id** (INT): Id of user.
        - **name** (STR): Name of user.
        - **contact** (STR): Contact of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **password** (STR): Password of user.
        - **is_admin** (BOOL): Is user admin or not.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling get_all_users method")

    query = select(func.count(UserTable.id)).where(UserTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    if page and limit:
        query = select(UserTable).where(and_(
            UserTable.is_deleted == False, UserTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "users fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [user.to_dict() for user in result]}},
            200, CONTENT_TYPE)


# Update a single user route
@user_router.put("/<int:user_id>/")
def update_user(
    user_id: int, db_session: Session = get_session()
):
    """
        Update a single user.

        Description:
        - This method is used to update a single user by providing id.
        - If any field is not provided, it will be updated with null value.

        Parameters:
        - **user_id** (INT): Id of user. *--Required*
        - **name** (STR): Name of user. *--Optional*
        - **contact** (STR): Contact of user. *--Optional*
        - **username** (STR): Username of user. *--Optional*
        - **email** (STR): Email of user. *--Optional*
        - **password** (STR): Password of user. *--Optional*

        Returns:
        user details along with following information:
        - **id** (INT): Id of user.
        - **name** (STR): Name of user.
        - **contact** (STR): Contact of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **password** (STR): Password of user.
        - **is_admin** (BOOL): Is user admin or not.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling update_user method")

    try:
        # Check if username already exists
        if request.json["username"]:
            query = select(UserTable).where(UserTable.username == request.json["username"])
            result = db_session.execute(query).first()

            if result:
                return ({"success": False, "message": "Username already exists", "data": None},
                        409, CONTENT_TYPE)

        # Check if email already exists
        if request.json["email"]:
            query = select(UserTable).where(UserTable.email == request.json["email"])
            result = db_session.execute(query).first()

            if result:
                return ({"success": False, "message": "Email already exists", "data": None},
                        409, CONTENT_TYPE)

        query = select(UserTable).where(and_(UserTable.id == user_id,
                                             UserTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        result.user_name = request.json.get("user_name", result.user_name)

        db_session.commit()

        return ({"success": True, "message": "user updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "user already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid user id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single user route
@user_router.delete("/<int:user_id>/")
def delete_user(
    user_id: int, db_session: Session = get_session()
):
    """
        Delete a single user.

        Description:
        - This method is used to delete a single user by providing id.

        Parameters:
        - **user_id** (INT): ID of user to be deleted. *--Required*

        Returns:
        - **message** (STR): User deleted successfully.

    """
    print("Calling delete_user method")

    query = select(UserTable).where(and_(UserTable.id == user_id,
                                         UserTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "User deleted successfully"},
            200, CONTENT_TYPE)
