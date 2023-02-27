"""
    Dashboard Module

    Description:
    - This module is responsible for getting dashboard data.

"""

# Importing Python packages
from sqlalchemy import (select, func, desc, text)
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


# Get dashboard data for user
@dashboard_router.get("/user/<int:user_id>/")
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
        - **booking_id** (STRING): Booking id.

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
                "booking_id": booking_detail.id
            })

        return ({"success": True, "message": "Dashboard data fetched successfully", "data": response},
                200, {"ContentType": "application/json"})

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": response},
                500, {"ContentType": "application/json"})


# get dashboard data for admin
@dashboard_router.get("/admin/<int:admin_id>/")
def get_dashboard_admin(
    admin_id, db_session: Session = get_session()
):
    """
        Get dashboard data based on admin id

        Description:
        - This method is used to get dashboard data based on admin id.

        Parameters:
        - **admin_id** (INT): Id of admin.

        Returns:
        Dashboard details along with following information:
        - **departure_location** (STRING): Departure location.
        - **departure_time** (STRING): Departure time.
        - **arrival_location** (STRING): Arrival location.
        - **arrival_time** (STRING): Arrival time.
        - **travel_type** (STRING): Travel type.
        - **class_type** (STRING): Class type.
        - **cost** (FLOAT): Cost of travel.
        - **booking_id** (STRING): Booking id.
        - **user_id** (INT): User id.
        - **user_name** (STRING): User name.

    """
    print("Calling get_dashboard_admin method")

    response = {
        "bookings": [],
        "monthly_revenue": {},
        "journey_revenue": {},
        "top_customers": []
    }

    try:
        # Get all users
        users = db_session.query(UserTable).where(
            UserTable.is_deleted == False).all()

        if not users:
            return ({"success": False, "message": "No users found", "data": response},
                    404, {"ContentType": "application/json"})

        # Loop through all users
        for user in users:
            # Get al booking details based on user id
            booking_details = db_session.query(BookingTable).filter(
                BookingTable.user_id == user.id, BookingTable.is_deleted == False).all()

            # Loop through all booking details
            if booking_details:
                for booking_detail in booking_details:
                    # Get travel detail based on travel detail id
                    travel_detail = db_session.query(TravelDetailTable).filter(
                        TravelDetailTable.id == booking_detail.travel_detail_id,
                        TravelDetailTable.is_deleted == False).first()

                    # Get travel type based on travel type id
                    travel_type = db_session.query(TravelTypeTable).filter(
                        TravelTypeTable.id == travel_detail.travel_type_id,
                        TravelTypeTable.is_deleted == False).first()

                    # Get departure location based on departure location id
                    departure_location = db_session.query(LocationTable).filter(
                        LocationTable.id == travel_detail.departure_location_id,
                        LocationTable.is_deleted == False).first()

                    # Get arrival location based on arrival location id
                    arrival_location = db_session.query(LocationTable).filter(
                        LocationTable.id == travel_detail.arrival_location_id,
                        LocationTable.is_deleted == False).first()

                    # Get expense based on expense id
                    expense = db_session.query(ExpenseTable).filter(
                        ExpenseTable.travel_detail_id == travel_detail.id,
                        ExpenseTable.is_deleted == False).first()

                    # Get price category based on price category id
                    price_category = db_session.query(PriceCategoryTable).filter(
                        PriceCategoryTable.id == expense.price_category_id,
                        PriceCategoryTable.is_deleted == False).first()

                    # Create response object
                    response["bookings"].append({
                        "departure_location": departure_location.name,
                        "departure_time": travel_detail.departure_time,
                        "arrival_location": arrival_location.name,
                        "arrival_time": travel_detail.arrival_time,
                        "travel_type": travel_type.name,
                        "class_type": price_category.name,
                        "cost": booking_detail.cost,
                        "booking_id": booking_detail.id,
                        "user_id": user.id,
                        "user_name": user.name
                    })

                    if booking_detail.created_at.strftime("%B %Y") in response["monthly_revenue"]:
                        response["monthly_revenue"][booking_detail.created_at.strftime(
                            "%B %Y")] += booking_detail.cost

                    else:
                        response["monthly_revenue"][booking_detail.created_at.strftime(
                            "%B %Y")] = booking_detail.cost

                    # Get journey revenue
                    journey = f"{departure_location.name} - {arrival_location.name} by {travel_type.name}"
                    if journey in response["journey_revenue"]:
                        response["journey_revenue"][journey] += booking_detail.cost

                    else:
                        response["journey_revenue"][journey] = booking_detail.cost

        query = """
                    SELECT user_id, COUNT(id) as booking_count
                    FROM horizontravels_database.booking
                    GROUP BY user_id
                    ORDER BY COUNT(id) DESC
                    LIMIT 5;
                """

        query = text(query)

        top_customers = db_session.execute(query).fetchall()

        for customer in top_customers:
            user = db_session.query(UserTable).filter(
                UserTable.id == customer[0],
                UserTable.is_deleted == False).first()
            response["top_customers"].append({
                "user_name": user.name,
                "booking_count": customer[1]
            })

        return ({"success": True, "message": "Dashboard data fetched successfully", "data": response},
                200, {"ContentType": "application/json"})

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": response},
                500, {"ContentType": "application/json"})
