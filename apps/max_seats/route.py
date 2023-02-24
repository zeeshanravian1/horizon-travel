"""
    Max Seats APIs Module

    Description:
    - This module is responsible for handling max seats APIs.
    - It is used to create, get, update, delete max seats details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (MAX_SEATS_NOT_FOUND)
from .model import (MaxSeatsTable)
from ..base import (CONTENT_TYPE)


max_seats_router = Blueprint(
    name="MaxSeatsRouter",
    import_name=__name__,
    url_prefix="/max_seats",
)


# --------------------------------------------------------------------------------------------------


# Create a single max seats
@max_seats_router.post("/")
def create_max_seats(
    db_session: Session = get_session()
):
    """
        Create a single max seats.

        Description:
        - This method is used to create a single max seats.

        Parameters:
        Max seats details to be created with following fields:
        - **seats** (INT): Number of seats. *--Required*
        - **travel_type_id** (INT): Id of travel type. *--Required*

        Returns:
        Max seats details along with following information:
        - **id** (INT): Id of max seats.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seats creation.
        - **updated_at** (DATETIME): Datetime of max seats updation.
    """
    print("Calling create_max_seats method")

    try:
        record = MaxSeatsTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Max seats created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Max seats for given travel type already exists",
                     "data": None}, 409, CONTENT_TYPE)

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


# Get a single max seats route
@max_seats_router.get("/<int:max_seats_id>/")
def get_max_seats(
    max_seats_id: int, db_session: Session = get_session()
):
    """
        Get a single max seats.

        Description:
        - This method is used to get a single max seats.

        Parameters:
        - **max_seats_id** (INT): Id of max seats. *--Required*

        Returns:
        Max seats details along with following information:
        - **id** (INT): Id of max seats.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seats creation.
        - **updated_at** (DATETIME): Datetime of max seats updation.

    """
    print("Calling get_max_seats method")

    query = select(MaxSeatsTable).where(and_(MaxSeatsTable.id == max_seats_id,
                                             MaxSeatsTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": MAX_SEATS_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "max seats fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all max seatss route
@max_seats_router.get("/")
def get_all_max_categories(
    page: int | None = 1, limit: int | None = 10,
    db_session: Session = get_session()
):
    """
        Get all max categories.

        Description:
        - This method is used to get all max categories.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all max categories with following information:
        - **id** (INT): Id of max seats.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seats creation.
        - **updated_at** (DATETIME): Datetime of max seats updation.

    """
    print("Calling get_all_max_categories method")

    query = select(func.count(MaxSeatsTable.id)).where(
        MaxSeatsTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    if page and limit:
        query = select(MaxSeatsTable).where(and_(
            MaxSeatsTable.is_deleted == False, MaxSeatsTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": MAX_SEATS_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "max seatss fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [max_seats.to_dict() for max_seats in result]}},
            200, CONTENT_TYPE)


# Update a single max seats route
@max_seats_router.put("/<int:travel_type_id>/")
def update_max_seats(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Update a single max seats.

        Description:
        - This method is used to update a single max seats by providing id.

        Parameters:
        - **travel_type_id** (INT): Id of max seats. *--Required*
        - **seats** (INT): Number of seats. *--Optional*

        Returns:
        max seats details along with following information:
        - **id** (INT): Id of max seats.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seats creation.
        - **updated_at** (DATETIME): Datetime of max seats updation.

    """
    print("Calling update_max_seats method")

    try:
        query = select(MaxSeatsTable).where(and_(MaxSeatsTable.travel_type_id == travel_type_id,
                                                    MaxSeatsTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": MAX_SEATS_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        if result.name == request.json["name"]:
            return ({"success": False, "message": "max seats already exists", "data": None},
                    409, CONTENT_TYPE)

        result.seats = request.json["seats"]

        db_session.commit()

        return ({"success": True, "message": "max seats updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "max seats already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid max seats id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single max seats route
@max_seats_router.delete("/<int:travel_type_id>/")
def delete_max_seats(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Delete a single max seats.

        Description:
        - This method is used to delete a single max seats by providing id.

        Parameters:
        - **travel_type_id** (INT): Id of max seats. *--Required*

        Returns:
        - **message** (STR): max seats deleted successfully.

    """
    print("Calling delete_max_seats method")

    query = select(MaxSeatsTable).where(and_(MaxSeatsTable.travel_type_id == travel_type_id,
                                                MaxSeatsTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": MAX_SEATS_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "max seats deleted successfully"},
            200, CONTENT_TYPE)
