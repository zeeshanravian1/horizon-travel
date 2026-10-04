"""
    Location APIs Module

    Description:
    - This module is responsible for handling location APIs.
    - It is used to create, get, update, delete location details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (LOCATION_NOT_FOUND)
from .model import (LocationTable)
from ..base import (CONTENT_TYPE)


location_router = Blueprint(
    name="LocationRouter",
    import_name=__name__,
    url_prefix="/location",
)


# --------------------------------------------------------------------------------------------------


# Create a single location
@location_router.post("/")
def create_location(
    db_session: Session = get_session()
):
    """
        Create a single location.

        Description:
        - This method is used to create a single location.

        Parameters:
        Location details to be created with following fields:
        - **name** (STR): Name of location. *--Required*
        - **longitude** (FLOAT): Longitude of location. *--Required*
        - **latitude** (FLOAT): Latitude of location. *--Required*

        Returns:
        Location details along with following information:
        - **id** (INT): Id of location.
        - **name** (STR): Name of location.
        - **longitude** (FLOAT): Longitude of location.
        - **latitude** (FLOAT): Latitude of location.
        - **created_at** (DATETIME): Datetime of location creation.
        - **updated_at** (DATETIME): Datetime of location updation.
    """

    try:
        record = LocationTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "location created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Location already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid location id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single location route
@location_router.get("/<int:location_id>/")
def get_location(
    location_id: int, db_session: Session = get_session()
):
    """
        Get a single location.

        Description:
        - This method is used to get a single location.

        Parameters:
        - **location_id** (INT): Id of location. *--Required*

        Returns:
        Location details along with following information:
        - **id** (INT): Id of location.
        - **name** (STR): Name of location.
        - **longitude** (FLOAT): Longitude of location.
        - **latitude** (FLOAT): Latitude of location.
        - **created_at** (DATETIME): Datetime of location creation.
        - **updated_at** (DATETIME): Datetime of location updation.

    """

    query = select(LocationTable).where(and_(LocationTable.id == location_id,
                                             LocationTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": LOCATION_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "location fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all locations route
@location_router.get("/")
def get_all_locations(
    page: int | None = None, limit: int | None = None,
    db_session: Session = get_session()
):
    """
        Get all locations.

        Description:
        - This method is used to get all locations.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all locations with following information:
        - **id** (INT): Id of location.
        - **name** (STR): Name of location.
        - **longitude** (FLOAT): Longitude of location.
        - **latitude** (FLOAT): Latitude of location.
        - **created_at** (DATETIME): Datetime of location creation.
        - **updated_at** (DATETIME): Datetime of location updation.

    """

    query = select(func.count(LocationTable.id)).where(
        LocationTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(LocationTable).where(LocationTable.is_deleted == False)

    if page and limit:
        query = select(LocationTable).where(and_(
            LocationTable.is_deleted == False, LocationTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": LOCATION_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)
    
    if not (page and limit):
        page = 1
        limit = total_count

    return ({"success": True, "message": "Locations fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [location.to_dict() for location in result]}},
            200, CONTENT_TYPE)


# Update a single location route
@location_router.put("/<int:location_id>/")
def update_location(
    location_id: int, db_session: Session = get_session()
):
    """
        Update a single location.

        Description:
        - This method is used to update a single location by providing id.

        Parameters:
        - **location_id** (INT): Id of location. *--Required*
        - **name** (STR): Name of location. *--Optional*
        - **longitude** (FLOAT): Longitude of location. *--Optional*
        - **latitude** (FLOAT): Latitude of location. *--Optional*

        Returns:
        Location details along with following information:
        - **id** (INT): Id of location.
        - **name** (STR): Name of location.
        - **longitude** (FLOAT): Longitude of location.
        - **latitude** (FLOAT): Latitude of location.
        - **created_at** (DATETIME): Datetime of location creation.
        - **updated_at** (DATETIME): Datetime of location updation.

    """

    try:
        query = select(LocationTable).where(and_(LocationTable.id == location_id,
                                                 LocationTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": LOCATION_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)
        
        if result.name == request.json["name"]:
            return ({"success": False, "message": "Location already exists", "data": None},
                    409, CONTENT_TYPE)

        result.name = request.json["name"]
        result.longitude = request.json["longitude"]
        result.latitude = request.json["latitude"]

        db_session.commit()

        return ({"success": True, "message": "location updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "location already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid location id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single location route
@location_router.delete("/<int:location_id>/")
def delete_location(
    location_id: int, db_session: Session = get_session()
):
    """
        Delete a single location.

        Description:
        - This method is used to delete a single location by providing id.

        Parameters:
        - **location_id** (INT): ID of location to be deleted. *--Required*

        Returns:
        - **message** (STR): Location deleted successfully.

    """

    query = select(LocationTable).where(and_(LocationTable.id == location_id,
                                             LocationTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": LOCATION_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "location deleted successfully"},
            200, CONTENT_TYPE)
