"""
    Travel Detail APIs Module

    Description:
    - This module is responsible for handling travel detail APIs.
    - It is used to create, get, update, delete travel detail details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (TRAVEL_DETAIL_NOT_FOUND)
from .model import (TravelDetailTable)
from ..base import (CONTENT_TYPE)


travel_detail_router = Blueprint(
    name="TravelDetailRouter",
    import_name=__name__,
    url_prefix="/travel_detail",
)


# --------------------------------------------------------------------------------------------------


# Create a single travel detail
@travel_detail_router.post("/")
def create_travel_detail(
    db_session: Session = get_session()
):
    """
        Create a single travel detail.

        Description:
        - This method is used to create a single travel detail.

        Parameters:
        travel detail details to be created with following fields:
        - **travel_type_id** (INT): Id of travel type. *--Required*
        - **departure_location_id** (INT): Id of departure location. *--Required*
        - **departure_time** (DATETIME): Datetime of departure. *--Required*
        - **arrival_location_id** (INT): Id of arrival location. *--Required*
        - **arrival_time** (DATETIME): Datetime of arrival. *--Required*

        Returns:
        travel detail details along with following information:
        - **id** (INT): Id of travel detail.
        - **travel_type_id** (INT): Id of travel type.
        - **departure_location_id** (INT): Id of departure location.
        - **departure_time** (DATETIME): Datetime of departure.
        - **arrival_location_id** (INT): Id of arrival location.
        - **arrival_time** (DATETIME): Datetime of arrival.
        - **created_at** (DATETIME): Datetime of travel detail creation.
        - **updated_at** (DATETIME): Datetime of travel detail updation.
    """

    try:
        record = TravelDetailTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Travel detail created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Travel detail already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid travel detail id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single travel detail route
@travel_detail_router.get("/<int:travel_detail_id>/")
def get_travel_detail(
    travel_detail_id: int, db_session: Session = get_session()
):
    """
        Get a single travel detail.

        Description:
        - This method is used to get a single travel detail.

        Parameters:
        - **travel_detail_id** (INT): Id of travel detail. *--Required*

        Returns:
        travel detail details along with following information:
        - **id** (INT): Id of travel detail.
        - **travel_type_id** (INT): Id of travel type.
        - **departure_location_id** (INT): Id of departure location.
        - **departure_time** (DATETIME): Datetime of departure.
        - **arrival_location_id** (INT): Id of arrival location.
        - **arrival_time** (DATETIME): Datetime of arrival.
        - **created_at** (DATETIME): Datetime of travel detail creation.
        - **updated_at** (DATETIME): Datetime of travel detail updation.

    """

    query = select(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
                                               TravelDetailTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": TRAVEL_DETAIL_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "Travel detail fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all travel details route
@travel_detail_router.get("/")
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
        - **id** (INT): Id of travel detail.
        - **travel_type_id** (INT): Id of travel type.
        - **departure_location_id** (INT): Id of departure location.
        - **departure_time** (DATETIME): Datetime of departure.
        - **arrival_location_id** (INT): Id of arrival location.
        - **arrival_time** (DATETIME): Datetime of arrival.
        - **created_at** (DATETIME): Datetime of travel detail creation.
        - **updated_at** (DATETIME): Datetime of travel detail updation.

    """

    query = select(func.count(TravelDetailTable.id)).where(
        TravelDetailTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(TravelDetailTable).where(TravelDetailTable.is_deleted == False)

    if page and limit:
        query = select(TravelDetailTable).where(and_(
            TravelDetailTable.is_deleted == False, TravelDetailTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": TRAVEL_DETAIL_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)
    
    if not (page and limit):
        page = 1
        limit = total_count

    return ({"success": True, "message": "Travel details fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [travel_detail.to_dict() for travel_detail in result]}},
            200, CONTENT_TYPE)


# Update a single travel detail route
@travel_detail_router.put("/<int:travel_detail_id>/")
def update_travel_detail(
    travel_detail_id: int, db_session: Session = get_session()
):
    """
        Update a single travel detail.

        Description:
        - This method is used to update a single travel detail by providing id.

        Parameters:
        - **travel_detail_id** (INT): Id of travel detail. *--Required*
        - **travel_type_id** (INT): Id of travel type. *--Optional*
        - **departure_location_id** (INT): Id of departure location. *--Optional*
        - **departure_time** (DATETIME): Datetime of departure. *--Optional*
        - **arrival_location_id** (INT): Id of arrival location. *--Optional*
        - **arrival_time** (DATETIME): Datetime of arrival. *--Optional*

        Returns:
        travel detail details along with following information:
        - **id** (INT): Id of travel detail.
        - **travel_type_id** (INT): Id of travel type.
        - **departure_location_id** (INT): Id of departure location.
        - **departure_time** (DATETIME): Datetime of departure.
        - **arrival_location_id** (INT): Id of arrival location.
        - **arrival_time** (DATETIME): Datetime of arrival.
        - **created_at** (DATETIME): Datetime of travel detail creation.
        - **updated_at** (DATETIME): Datetime of travel detail updation.

    """

    try:
        query = select(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
                                                   TravelDetailTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": TRAVEL_DETAIL_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        if result.name == request.json["name"]:
            return ({"success": False, "message": "Travel detail already exists", "data": None},
                    409, CONTENT_TYPE)

        result.travel_type_id = request.json["travel_type_id"]
        result.departure_location_id = request.json["departure_location_id"]
        result.departure_time = request.json["departure_time"]
        result.arrival_location_id = request.json["arrival_location_id"]
        result.arrival_time = request.json["arrival_time"]

        db_session.commit()

        return ({"success": True, "message": "Travel detail updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Travel detail already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid travel detail id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single travel detail route
@travel_detail_router.delete("/<int:travel_detail_id>/")
def delete_travel_detail(
    travel_detail_id: int, db_session: Session = get_session()
):
    """
        Delete a single travel detail.

        Description:
        - This method is used to delete a single travel detail by providing id.

        Parameters:
        - **travel_detail_id** (INT): ID of travel detail to be deleted. *--Required*

        Returns:
        - **message** (STR): travel detail deleted successfully.

    """

    query = select(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
                                               TravelDetailTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": TRAVEL_DETAIL_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "Travel detail deleted successfully"},
            200, CONTENT_TYPE)
