"""
    Price Category APIs Module

    Description:
    - This module is responsible for handling price category APIs.
    - It is used to create, get, update, delete price category details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (PRICE_CATEGORY_NOT_FOUND)
from .model import (PriceCategoryTable)
from ..base import (CONTENT_TYPE)


price_category_router = Blueprint(
    name="PriceCategoryRouter",
    import_name=__name__,
    url_prefix="/price_category",
)


# --------------------------------------------------------------------------------------------------


# Create a single price category
@price_category_router.post("/")
def create_price_category(
    db_session: Session = get_session()
):
    """
        Create a single price category.

        Description:
        - This method is used to create a single price category.

        Parameters:
        price category details to be created with following fields:
        - **name** (STR): Name of price category. *--Required*

        Returns:
        price category details along with following information:
        - **id** (INT): Id of price category.
        - **name** (STR): Name of price category.
        - **created_at** (DATETIME): Datetime of price category creation.
        - **updated_at** (DATETIME): Datetime of price category updation.
    """
    print("Calling create_price_category method")

    try:
        record = PriceCategoryTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Price category created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Price category already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid price category id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single price category route
@price_category_router.get("/<int:price_category_id>/")
def get_price_category(
    price_category_id: int, db_session: Session = get_session()
):
    """
        Get a single price category.

        Description:
        - This method is used to get a single price category.

        Parameters:
        - **price_category_id** (INT): Id of price category. *--Required*

        Returns:
        price category details along with following information:
        - **id** (INT): Id of price category.
        - **name** (STR): Name of price category.
        - **created_at** (DATETIME): Datetime of price category creation.
        - **updated_at** (DATETIME): Datetime of price category updation.

    """
    print("Calling get_price_category method")

    query = select(PriceCategoryTable).where(and_(PriceCategoryTable.id == price_category_id,
                                             PriceCategoryTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": PRICE_CATEGORY_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "price category fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all price categorys route
@price_category_router.get("/")
def get_all_price_categories(
    page: int | None = 1, limit: int | None = 10,
    db_session: Session = get_session()
):
    """
        Get all price categories.

        Description:
        - This method is used to get all price categories.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all price categories with following information:
        - **id** (INT): Id of price category.
        - **name** (STR): Name of price category.
        - **created_at** (DATETIME): Datetime of price category creation.
        - **updated_at** (DATETIME): Datetime of price category updation.

    """
    print("Calling get_all_price_categories method")

    query = select(func.count(PriceCategoryTable.id)).where(
        PriceCategoryTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    if page and limit:
        query = select(PriceCategoryTable).where(and_(
            PriceCategoryTable.is_deleted == False, PriceCategoryTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": PRICE_CATEGORY_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "price categorys fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [price_category.to_dict() for price_category in result]}},
            200, CONTENT_TYPE)


# Update a single price category route
@price_category_router.put("/<int:price_category_id>/")
def update_price_category(
    price_category_id: int, db_session: Session = get_session()
):
    """
        Update a single price category.

        Description:
        - This method is used to update a single price category by providing id.

        Parameters:
        - **price category_id** (INT): Id of price category. *--Required*
        - **name** (STR): Name of price category. *--Optional*

        Returns:
        price category details along with following information:
        - **id** (INT): Id of price category.
        - **name** (STR): Name of price category.
        - **created_at** (DATETIME): Datetime of price category creation.
        - **updated_at** (DATETIME): Datetime of price category updation.

    """
    print("Calling update_price_category method")

    try:
        query = select(PriceCategoryTable).where(and_(PriceCategoryTable.id == price_category_id,
                                                 PriceCategoryTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": PRICE_CATEGORY_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        if result.name == request.json["name"]:
            return ({"success": False, "message": "Price category already exists", "data": None},
                    409, CONTENT_TYPE)

        result.name = request.json["name"]
        result.longitude = request.json["longitude"]
        result.latitude = request.json["latitude"]

        db_session.commit()

        return ({"success": True, "message": "Price category updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Price category already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid price category id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single price category route
@price_category_router.delete("/<int:price_category_id>/")
def delete_price_category(
    price_category_id: int, db_session: Session = get_session()
):
    """
        Delete a single price category.

        Description:
        - This method is used to delete a single price category by providing id.

        Parameters:
        - **price_category_id** (INT): ID of price category to be deleted. *--Required*

        Returns:
        - **message** (STR): price category deleted successfully.

    """
    print("Calling delete_price_category method")

    query = select(PriceCategoryTable).where(and_(PriceCategoryTable.id == price_category_id,
                                             PriceCategoryTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": PRICE_CATEGORY_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "price category deleted successfully"},
            200, CONTENT_TYPE)
