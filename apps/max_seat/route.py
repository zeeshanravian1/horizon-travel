"""
    Max Seat APIs Module

    Description:
    - This module is responsible for handling max seat APIs.
    - It is used to create, get, update, delete max seat details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (MAX_SEAT_NOT_FOUND)
from .model import (MaxSeatTable)
from ..base import (CONTENT_TYPE)


max_seat_router = Blueprint(
    name="MaxSeatRouter",
    import_name=__name__,
    url_prefix="/max_seat",
)


# --------------------------------------------------------------------------------------------------


# Create a single max seat
@max_seat_router.post("/")
def create_max_seat(
    db_session: Session = get_session()
):
    """
        Create a single max seat.

        Description:
        - This method is used to create a single max seat.

        Parameters:
        Max seat details to be created with following fields:
        - **seats** (INT): Number of seats. *--Required*
        - **travel_type_id** (INT): Id of travel type. *--Required*

        Returns:
        Max seat details along with following information:
        - **id** (INT): Id of max seat.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seat creation.
        - **updated_at** (DATETIME): Datetime of max seat updation.
    """

    try:
        record = MaxSeatTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Max seat created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Max seat for given travel type already exists",
                     "data": None}, 409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid travel type id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single max seat route
@max_seat_router.get("/<int:travel_type_id>/")
def get_max_seat(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Get a single max seat.

        Description:
        - This method is used to get a single max seat.

        Parameters:
        - **travel_type_id** (INT): Id of travel type. *--Required*

        Returns:
        Max seat details along with following information:
        - **id** (INT): Id of max seat.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seat creation.
        - **updated_at** (DATETIME): Datetime of max seat updation.

    """

    query = select(MaxSeatTable).where(and_(MaxSeatTable.travel_type_id == travel_type_id,
                                            MaxSeatTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": MAX_SEAT_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "Max seat fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all max seats route
@max_seat_router.get("/")
def get_all_max_seats(
    page: int | None = None, limit: int | None = None,
    db_session: Session = get_session()
):
    """
        Get all max seats.

        Description:
        - This method is used to get all max categories.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all max categories with following information:
        - **id** (INT): Id of max seat.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seat creation.
        - **updated_at** (DATETIME): Datetime of max seat updation.

    """

    query = select(func.count(MaxSeatTable.id)).where(
        MaxSeatTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(MaxSeatTable).where(MaxSeatTable.is_deleted == False)

    if page and limit:
        query = select(MaxSeatTable).where(and_(
            MaxSeatTable.is_deleted == False, MaxSeatTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": MAX_SEAT_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)
    
    if not (page and limit):
        page = 1
        limit = total_count

    return ({"success": True, "message": "max seats fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [max_seat.to_dict() for max_seat in result]}},
            200, CONTENT_TYPE)


# Update a single max seat route
@max_seat_router.put("/<int:travel_type_id>/")
def update_max_seat(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Update a single max seat.

        Description:
        - This method is used to update a single max seat by providing id.

        Parameters:
        - **travel_type_id** (INT): Id of travel type. *--Required*
        - **seat** (INT): Number of seat. *--Optional*

        Returns:
        Max seat details along with following information:
        - **id** (INT): Id of max seat.
        - **seats** (INT): Number of seats.
        - **travel_type_id** (INT): Id of travel type.
        - **created_at** (DATETIME): Datetime of max seat creation.
        - **updated_at** (DATETIME): Datetime of max seat updation.

    """

    try:
        query = select(MaxSeatTable).where(and_(MaxSeatTable.travel_type_id == travel_type_id,
                                                    MaxSeatTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": MAX_SEAT_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        if result.name == request.json["name"]:
            return ({"success": False, "message": "max seat already exists", "data": None},
                    409, CONTENT_TYPE)

        result.seats = request.json["seats"]

        db_session.commit()

        return ({"success": True, "message": "Max seat updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Max seat already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid max seat id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single max seat route
@max_seat_router.delete("/<int:travel_type_id>/")
def delete_max_seat(
    travel_type_id: int, db_session: Session = get_session()
):
    """
        Delete a single max seat.

        Description:
        - This method is used to delete a single max seat by providing id.

        Parameters:
        - **travel_type_id** (INT): Id of travel type. *--Required*

        Returns:
        - **message** (STR): Max seat deleted successfully.

    """

    query = select(MaxSeatTable).where(and_(MaxSeatTable.travel_type_id == travel_type_id,
                                                MaxSeatTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": MAX_SEAT_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "Max seat deleted successfully"},
            200, CONTENT_TYPE)
