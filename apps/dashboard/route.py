"""
    Dashboard Module

    Description:
    - This module is responsible for getting dashboard data.

"""

# Importing Python packages
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
from apps.booking.model import (BookingTable)
from apps.user.model import (UserTable)


dashboard_router = Blueprint(
    name="dashboard",
    import_name=__name__,
    url_prefix="/dashboard",
)


# --------------------------------------------------------------------------------------------------


# Create a single location
@dashboard_router.get("/<int:user_id>/")
def get_dashboard(
    user_id, db_session: Session = get_session()
):
    """
        Get dashboard data based on user id

        Description:
        - This method is used to get dashboard data based on user id.

        Parameters:
        - **user_id** (INT): Id of user.

        Returns:
        Dashboard details along with following information:
        - **departure_location** (STRING): Departure location.
        - **departure_time** (STRING): Departure time.
        - **arrival_location** (STRING): Arrival location.
        - **arrival_time** (STRING): Arrival time.
        - **travel_type** (STRING): Travel type.
        - **class_type** (STRING): Class type.
        - **cost** (FLOAT): Cost of travel.
        - **receipt** (STRING): Receipt of travel.

    """
    print("Calling get_dashboard method")

    response = []

    try:
        # Get User Details
        user_details = db_session.query(UserTable).filter(
            UserTable.id == user_id).first()

        if not user_details:
            return ({"success": False, "message": "User not found", "data": response},
                    404, {"ContentType": "application/json"})

        # Get al booking details based on user id
        booking_details = db_session.query(BookingTable).filter(
            BookingTable.user_id == user_id).all()
        
        if not booking_details:
            return ({"success": False, "message": "No bookings found", "data": response},
                    404, {"ContentType": "application/json"})
        
        # Loop through all booking details
        for booking_detail in booking_details:
            # Get travel detail based on travel detail id
            travel_detail = db_session.query(TravelDetailTable).filter(
                TravelDetailTable.id == booking_detail.travel_detail_id).first()

            # Get travel type based on travel type id
            travel_type = db_session.query(TravelTypeTable).filter(
                TravelTypeTable.id == travel_detail.travel_type_id).first()

            # Get departure location based on departure location id
            departure_location = db_session.query(LocationTable).filter(
                LocationTable.id == travel_detail.departure_location_id).first()

            # Get arrival location based on arrival location id
            arrival_location = db_session.query(LocationTable).filter(
                LocationTable.id == travel_detail.arrival_location_id).first()

            # Get expense based on expense id
            expense = db_session.query(ExpenseTable).filter(
                ExpenseTable.travel_detail_id == travel_detail.id).first()

            # Get price category based on price category id
            price_category = db_session.query(PriceCategoryTable).filter(
                PriceCategoryTable.id == expense.price_category_id).first()

            # Create response object
            response.append({
                "departure_location": departure_location.name,
                "departure_time": travel_detail.departure_time,
                "arrival_location": arrival_location.name,
                "arrival_time": travel_detail.arrival_time,
                "travel_type": travel_type.name,
                "class_type": price_category.name,
                "cost": booking_detail.cost,
                "receipt": ""
            })

        return ({"success": True, "message": "Dashboard data fetched successfully", "data": response},
                200, {"ContentType": "application/json"})


    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": response},
                500, {"ContentType": "application/json"})
