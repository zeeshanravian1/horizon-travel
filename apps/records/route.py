"""
    Records Module

    Description:
    - This module is responsible for getting records data.

"""

# Importing Python packages
from datetime import (datetime)
from sqlalchemy import (select, and_)
from sqlalchemy.orm import (Session)

# Importing Flask packages
from flask import (Blueprint)

# Importing from project files
from database.session import (get_session)
from apps.location.model import (LocationTable)
from apps.travel_type.model import (TravelTypeTable)
from apps.travel_detail.model import (TravelDetailTable)
from apps.expense.model import (ExpenseTable)
from apps.price_category.model import (PriceCategoryTable)


records_router = Blueprint(
    name="Records",
    import_name=__name__,
    url_prefix="/records",
)


# --------------------------------------------------------------------------------------------------


# Create a single location
@records_router.get("/<travel_type>/<departure_location>/<arrival_location>/")
def get_records(
    travel_type: str = None, departure_location: str = None, arrival_location: str = None,
    db_session: Session = get_session()
):
    """
        Get data based on user filters

        Description:
        - This method is used to geta data based on user filters.

        Parameters:
        - **travel_type** (STR): Travel type.
        - **departure_location** (STR): Departure location.
        - **arrival_location** (STR): Arrival location.

        Returns:
        Location details along with following information:
        - **id** (INT): Id of location.
        - **name** (STR): Name of location.
        - **longitude** (FLOAT): Longitude of location.
        - **latitude** (FLOAT): Latitude of location.
        - **created_at** (DATETIME): Datetime of location creation.
        - **updated_at** (DATETIME): Datetime of location updation.

    """
    print("Calling get_homepage method")

    response = []

    try:
        travel_type = travel_type.lower()
        departure_location = departure_location.lower()
        arrival_location = arrival_location.lower()

        query = select(LocationTable).where(LocationTable.is_deleted == False)
        result = db_session.execute(query).scalars().all()

        if result:
            locations = {location.name.lower(): location.id for location in result}

        query = select(TravelTypeTable).where(TravelTypeTable.is_deleted == False)
        result = db_session.execute(query).scalars().all()

        if result:
            travel_types = {travel_type.name.lower(): travel_type.id for travel_type in result}

        query = select(TravelDetailTable).where(and_(
            TravelDetailTable.is_deleted == False,
            TravelDetailTable.travel_type_id == travel_types[travel_type],
            TravelDetailTable.departure_location_id == locations[departure_location],
            TravelDetailTable.arrival_location_id == locations[arrival_location]))

        result = db_session.execute(query).scalars().all()

        if result:
            travel_details = {travel_detail.id: {
                "departure_location": departure_location.capitalize(),
                "departure_time": travel_detail.departure_time.strftime("%Y-%m-%d %H:%M:%S"),
                "arrival_location": arrival_location.capitalize(),
                "arrival_time": travel_detail.arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
            } for travel_detail in result}

        query = select(ExpenseTable).where(and_(
            ExpenseTable.is_deleted == False,
            ExpenseTable.travel_detail_id.in_(travel_details.keys())))

        result = db_session.execute(query).scalars().all()

        if result:
            expenses = [expense.to_dict() for expense in result]

        query = select(PriceCategoryTable).where(
            PriceCategoryTable.is_deleted == False,
            PriceCategoryTable.id.in_([expense["price_category_id"] for expense in expenses]))

        result = db_session.execute(query).scalars().all()

        if result:
            price_categories = {price_category.id: {
                "name": price_category.name,
            } for price_category in result}

        for expense in expenses:
            expense["class_type"] = price_categories[expense["price_category_id"]]["name"]
            expense["departure_location"] = travel_details[expense["travel_detail_id"]]["departure_location"]
            expense["departure_time"] = travel_details[expense["travel_detail_id"]]["departure_time"]
            expense["arrival_location"] = travel_details[expense["travel_detail_id"]]["arrival_location"]
            expense["arrival_time"] = travel_details[expense["travel_detail_id"]]["arrival_time"]
            expense["discounted_cost"] = expense["cost"]

            difference = (datetime.strptime(expense["arrival_time"], "%Y-%m-%d %H:%M:%S") - datetime.now()).days

            if difference > 80 and difference < 90:
                expense["discounted_cost"] = expense["cost"] * 0.8
            elif difference > 60 and difference < 80:
                expense["discounted_cost"] = expense["cost"] * 0.9
            elif difference > 46 and difference < 60:
                expense["discounted_cost"] = expense["cost"] * 0.95

            del expense["id"]
            del expense["is_deleted"]
            del expense["created_at"]
            del expense["updated_at"]
            del expense["price_category_id"]
            del expense["travel_detail_id"]

        # sort by cost
        expenses = sorted(expenses, key=lambda k: k['cost'])

        response = expenses

        return ({"success": True, "message": "Data fetched successfully", "data": response},
                200, {"ContentType": "application/json"})

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": response},
                500, {"ContentType": "application/json"})
