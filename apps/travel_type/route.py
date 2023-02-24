"""
    Travel Type APIs Module

    Description:
    - This module is responsible for handling travel type APIs.
    - It is used to create, get, update, delete travel type details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (TRAVEL_TYPE_NOT_FOUND)
from .model import (TravelTypeTable)
from ..base import (CONTENT_TYPE)


travel_type_router = Blueprint(
    name="TravelTypeRouter",
    import_name=__name__,
    url_prefix="/travel_type",
)


# --------------------------------------------------------------------------------------------------


# Create a single travel type
@travel_type_router.post("/")
def create_travel_type(
    db_session: Session = get_session()
):
    """
        Create a single travel type.

        Description:
        - This method is used to create a single travel type.

        Parameters:
        travel type details to be created with following fields:
        - **name** (STR): Name of travel type. *--Required*

        Returns:
        travel type details along with following information:
        - **id** (INT): Id of travel type.
        - **name** (STR): Name of travel type.
        - **created_at** (DATETIME): Datetime of travel type creation.
        - **updated_at** (DATETIME): Datetime of travel type updation.
    """
    print("Calling create_travel_type method")

    try:
        record = TravelTypeTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Travel type created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Travel type already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid travel type id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single travel type route
@travel_type_router.get("/<int:travel_type_id>/")
def get_travel_type(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Get a single travel type.

        Description:
        - This method is used to get a single travel type.

        Parameters:
        - **travel_type_id** (INT): Id of travel type. *--Required*

        Returns:
        travel type details along with following information:
        - **id** (INT): Id of travel type.
        - **name** (STR): Name of travel type.
        - **created_at** (DATETIME): Datetime of travel type creation.
        - **updated_at** (DATETIME): Datetime of travel type updation.

    """
    print("Calling get_travel_type method")

    query = select(TravelTypeTable).where(and_(TravelTypeTable.id == travel_type_id,
                                               TravelTypeTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": TRAVEL_TYPE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "Travel type fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all travel types route
@travel_type_router.get("/")
def get_all_travel_categories(
    page: int | None = None, limit: int | None = None,
    db_session: Session = get_session()
):
    """
        Get all travel categories.

        Description:
        - This method is used to get all travel categories.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all travel categories with following information:
        - **id** (INT): Id of travel type.
        - **name** (STR): Name of travel type.
        - **created_at** (DATETIME): Datetime of travel type creation.
        - **updated_at** (DATETIME): Datetime of travel type updation.

    """
    print("Calling get_all_travel_categories method")

    query = select(func.count(TravelTypeTable.id)).where(
        TravelTypeTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(TravelTypeTable).where(TravelTypeTable.is_deleted == False)

    if page and limit:
        query = select(TravelTypeTable).where(and_(
            TravelTypeTable.is_deleted == False, TravelTypeTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": TRAVEL_TYPE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)
    
    if not (page and limit):
        page = 1
        limit = total_count

    return ({"success": True, "message": "Travel types fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [travel_type.to_dict() for travel_type in result]}},
            200, CONTENT_TYPE)


# Update a single travel type route
@travel_type_router.put("/<int:travel_type_id>/")
def update_travel_type(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Update a single travel type.

        Description:
        - This method is used to update a single travel type by providing id.

        Parameters:
        - **travel_type_id** (INT): Id of travel type. *--Required*
        - **name** (STR): Name of travel type. *--Optional*

        Returns:
        travel type details along with following information:
        - **id** (INT): Id of travel type.
        - **name** (STR): Name of travel type.
        - **created_at** (DATETIME): Datetime of travel type creation.
        - **updated_at** (DATETIME): Datetime of travel type updation.

    """
    print("Calling update_travel_type method")

    try:
        query = select(TravelTypeTable).where(and_(TravelTypeTable.id == travel_type_id,
                                                   TravelTypeTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": TRAVEL_TYPE_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        if result.name == request.json["name"]:
            return ({"success": False, "message": "Travel type already exists", "data": None},
                    409, CONTENT_TYPE)

        result.name = request.json["name"]

        db_session.commit()

        return ({"success": True, "message": "Travel type updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Travel type already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid travel type id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single travel type route
@travel_type_router.delete("/<int:travel_type_id>/")
def delete_travel_type(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Delete a single travel type.

        Description:
        - This method is used to delete a single travel type by providing id.

        Parameters:
        - **travel_type_id** (INT): ID of travel type to be deleted. *--Required*

        Returns:
        - **message** (STR): travel type deleted successfully.

    """
    print("Calling delete_travel_type method")

    query = select(TravelTypeTable).where(and_(TravelTypeTable.id == travel_type_id,
                                               TravelTypeTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": TRAVEL_TYPE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "Travel type deleted successfully"},
            200, CONTENT_TYPE)
