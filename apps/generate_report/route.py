"""
    Generate Report Route

    Description:
    - This module is responsible for generating reports.

"""

# Importing Python packages
from sqlalchemy.orm import (Session)

# Importing Flask packages
from flask import (Blueprint, make_response)

# Importing from project files
from database.session import (get_session)
from apps.location.model import (LocationTable)
from apps.travel_type.model import (TravelTypeTable)
from apps.travel_detail.model import (TravelDetailTable)
from apps.expense.model import (ExpenseTable)
from apps.price_category.model import (PriceCategoryTable)
from apps.booking.model import (BookingTable)
from apps.user.model import (UserTable)

from helper import (generatereport)

report_router = Blueprint(
    name="GenerateReport",
    import_name=__name__,
    url_prefix="/generate_report",
)


# --------------------------------------------------------------------------------------------------


# Generate Report based on booking id route
@report_router.route("/<int:booking_id>/", methods=["GET"])
def generate_report(
    booking_id: int, db_session: Session = get_session()
):
    """
        Generate Report based on booking id route

        Description:
        - This route is responsible for generating a report based on the booking id.

        Parameters:
        - booking_id (int): The booking id of the report to be generated.

        Returns:
        - Report PDF with following information:
        - **name** (str): The name of the user.
        - **email** (str): The email of the user.
        - **username** (str): The username of the user.
        - **departure_location** (str): The departure location of the travel.
        - **departure_time** (str): The departure time of the travel.
        - **arrival_location** (str): The arrival location of the travel.
        - **arrival_time** (str): The arrival time of the travel.
        - **travel_type** (str): The travel type of the travel.
        - **price_category** (str): The price category of the travel.
        - **cost** (str): The cost of the travel.

    """

    try:
        # Get the booking details
        booking_details = db_session.query(BookingTable).filter(
            BookingTable.id == booking_id, BookingTable.is_deleted == False).first()
        
        # Get the user details
        user_details = db_session.query(UserTable).filter(
            UserTable.id == booking_details.user_id, UserTable.is_deleted == False).first()
        
        # Get the travel details
        travel_details = db_session.query(TravelDetailTable).filter(
            TravelDetailTable.id == booking_details.travel_detail_id,
            TravelDetailTable.is_deleted == False).first()
        
        # Get the travel type details
        travel_type_details = db_session.query(TravelTypeTable).filter(
            TravelTypeTable.id == travel_details.travel_type_id,
            TravelTypeTable.is_deleted == False).first()
        
        # Get the price category details
        expense_details = db_session.query(ExpenseTable).filter(
            ExpenseTable.travel_detail_id == travel_details.id,
            ExpenseTable.is_deleted == False).first()
        
        # Get the price category details
        price_category_details = db_session.query(PriceCategoryTable).filter(
            PriceCategoryTable.id == expense_details.price_category_id,
            PriceCategoryTable.is_deleted == False).first()
        
        # Get the departure location details
        departure_location_details = db_session.query(LocationTable).filter(
            LocationTable.id == travel_details.departure_location_id,
            LocationTable.is_deleted == False).first()
        
        # Get the arrival location details
        arrival_location_details = db_session.query(LocationTable).filter(
            LocationTable.id == travel_details.arrival_location_id,
            LocationTable.is_deleted == False).first()
        
        user_details = {
            "Name": user_details.name,
            "Email": user_details.email,
            "Username": user_details.username
        }

        booking_details = {
            "Departure Location": departure_location_details.name,
            "Departure Time": travel_details.departure_time,
            "Arrival Location": arrival_location_details.name,
            "Arrival Time": travel_details.arrival_time,
            "Travel Type": travel_type_details.name.capitalize(),
            "Price Category": price_category_details.name.capitalize(),
            "Cost": booking_details.cost
        }

        buffer = generatereport(user_details, booking_details)
        pdf_output = buffer.getvalue()

        response = make_response(pdf_output)

        filename = f"{user_details['Username']}.pdf"

        # set the response headers to suggest that this is a PDF and to give it a filename
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, {"ContentType": "application/json"})
