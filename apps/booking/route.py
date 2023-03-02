"""
    Booking APIs Module

    Description:
    - This module is responsible for handling booking APIs.
    - It is used to create, get, update, delete booking details.

"""

# Importing Python packages
from datetime import (datetime)
from sqlalchemy import (select, update, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request, redirect, url_for, flash, render_template)
from flask_login import (login_required, current_user)

# Importing from project files
from database.session import (get_session)
from .exception import (BOOKING_NOT_FOUND)
from .model import (BookingTable)
from ..base import (CONTENT_TYPE)
from .form import (UpdateBookingForm)

from apps.travel_type.model import (TravelTypeTable)
from apps.location.model import (LocationTable)
from apps.travel_detail.model import (TravelDetailTable)
from apps.price_category.model import (PriceCategoryTable)
from apps.expense.model import (ExpenseTable)


booking_router = Blueprint(
    name="BookingRouter",
    import_name=__name__,
    url_prefix="/booking",
)


# --------------------------------------------------------------------------------------------------


# Create a single booking
@booking_router.post("/")
def create_booking(
    db_session: Session = get_session()
):
    """
        Create a single booking.

        Description:
        - This method is used to create a single booking.

        Parameters:
        Booking details to be created with following fields:
        - **user_id** (INT): Id of user. *--Required*
        - **travel_detail_id** (INT): Id of travel detail. *--Required*
        - **cost** (FLOAT): Cost of booking. *--Required*
        - **status** (ENUM): Status of booking. *--Required*
        - **refund_amount** (FLOAT): Refund amount of booking. *--Optional*

        Returns:
        Booking details along with following information:
        - **id** (INT): Id of booking.
        - **user_id** (INT): Id of user.
        - **travel_detail_id** (INT): Id of travel detail.
        - **cost** (FLOAT): Cost of booking.
        - **status** (ENUM): Status of booking.
        - **refund_amount** (FLOAT): Refund amount of booking.
        - **created_at** (DATETIME): Datetime of booking creation.
        - **updated_at** (DATETIME): Datetime of booking updation.

    """
    print("Calling create_booking method")

    try:
        print(request.form['class_type_id'], request.form['travel_detail_id'])

        # get travel detail
        travel_detail = db_session.query(TravelDetailTable).filter(
            TravelDetailTable.id == request.form['travel_detail_id'],
            TravelDetailTable.is_deleted == False).first()

        # Get expense
        expense = db_session.query(ExpenseTable).filter(
            ExpenseTable.travel_detail_id == request.form['travel_detail_id'],
            ExpenseTable.is_deleted == False).first()

        cost = expense.cost

        difference = (travel_detail.arrival_time - datetime.now()).days

        if difference > 80 and difference < 90:
            cost *= 0.8
        elif difference > 60 and difference < 80:
            cost *= 0.9
        elif difference > 46 and difference < 60:
            cost *= 0.95

        # insert into booking table
        record = BookingTable(
            user_id=None,
            travel_detail_id=request.form['travel_detail_id'],
            cost=cost,
            status="success",
            refund_amount=0.0
        )

        if current_user.is_authenticated:
            # insert into booking table
            record = BookingTable(
                user_id=current_user.id,
                travel_detail_id=request.form['travel_detail_id'],
                cost=cost,
                status="success",
                refund_amount=0.0
            )

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        if current_user.is_authenticated:
            return redirect(url_for('dashboard.get_dashboard'))
        else:
            return redirect(url_for('AuthenticationRouter.login', booking_id=record.id))

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Booking already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid booking id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single booking route
# @booking_router.get("/<int:booking_id>/")
# def get_booking(
#     booking_id: int, db_session: Session = get_session()
# ):
    """
        Get a single booking.

        Description:
        - This method is used to get a single booking.

        Parameters:
        - **booking_id** (INT): Id of booking. *--Required*

        Returns:
        Booking details along with following information:
        - **id** (INT): Id of booking.
        - **user_id** (INT): Id of user.
        - **travel_detail_id** (INT): Id of travel detail.
        - **cost** (FLOAT): Cost of booking.
        - **status** (ENUM): Status of booking.
        - **refund_amount** (FLOAT): Refund amount of booking.
        - **created_at** (DATETIME): Datetime of booking creation.
        - **updated_at** (DATETIME): Datetime of booking updation.

    """
    print("Calling get_booking method")

    query = select(BookingTable).where(and_(BookingTable.id == booking_id,
                                            BookingTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": BOOKING_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "booking fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all bookings route
@booking_router.route("/", methods=["GET"])
def get_all_bookings(
    db_session: Session = get_session()
):
    """
        Get all bookings.

        Description:
        - This method is used to get all bookings.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all bookings with following information:
        - **id** (INT): Id of booking.
        - **user_id** (INT): Id of user.
        - **travel_detail_id** (INT): Id of travel detail.
        - **cost** (FLOAT): Cost of booking.
        - **status** (ENUM): Status of booking.
        - **refund_amount** (FLOAT): Refund amount of booking.
        - **created_at** (DATETIME): Datetime of booking creation.
        - **updated_at** (DATETIME): Datetime of booking updation.

    """
    print("Calling get_all_bookings method")

    if not current_user.is_authenticated:
        return redirect(url_for('AuthenticationRouter.login'))

    page = request.args.get('page', None)
    limit = request.args.get('limit', None)

    query = select(func.count(BookingTable.id)).where(
        BookingTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(BookingTable).where(BookingTable.is_deleted == False,
                                       BookingTable.user_id == current_user.id)

    if page and limit:
        query = select(BookingTable).where(and_(
            BookingTable.is_deleted == False, BookingTable.user_id == current_user.id,
            BookingTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()
    print(result)
    if not result:
        return ({"success": False, "message": BOOKING_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    if not (page and limit):
        page = 1
        limit = total_count

    return render_template('bookings_list.html', bookings=result, my_bookings=True)


# Update a single booking route
@booking_router.route("/update/<int:booking_id>/", methods=["POST", "GET"])
@login_required
def update_booking(
    booking_id: int, db_session: Session = get_session()
):
    """
        Update a single booking.

        Description:
        - This method is used to update a single booking by providing id.

        Parameters:
        - **booking_id** (INT): Id of booking. *--Required*
        - **user_id** (INT): Id of user. *--Optional*
        - **travel_detail_id** (INT): Id of travel detail. *--Optional*
        - **cost** (FLOAT): Cost of booking. *--Optional*
        - **status** (ENUM): Status of booking. *--Optional*
        - **refund_amount** (FLOAT): Refund amount of booking. *--Optional*

        Returns:
        booking details along with following information:
        - **id** (INT): Id of booking.
        - **user_id** (INT): Id of user.
        - **travel_detail_id** (INT): Id of travel detail.
        - **cost** (FLOAT): Cost of booking.
        - **status** (ENUM): Status of booking.
        - **refund_amount** (FLOAT): Refund amount of booking.
        - **created_at** (DATETIME): Datetime of booking creation.
        - **updated_at** (DATETIME): Datetime of booking updation.

    """
    print("Calling update_booking method")

    try:
        if request.method == "GET":
            response = {}
            form = UpdateBookingForm()

            query = select(BookingTable).where(and_(BookingTable.id == booking_id,
                                                    BookingTable.is_deleted == False))

            record = db_session.execute(statement=query).scalar_one_or_none()

            if record is None:
                return ({"success": False, "message": BOOKING_NOT_FOUND, "data": None},
                        404, CONTENT_TYPE)

            # get travel details
            query = select(TravelDetailTable).where(and_(TravelDetailTable.id == record.travel_detail_id,
                                                    TravelDetailTable.is_deleted == False))

            travel_detail = db_session.execute(
                statement=query).scalar_one_or_none()

            # get travel type
            query = select(TravelTypeTable).where(and_(TravelTypeTable.id == travel_detail.travel_type_id,
                                                    TravelTypeTable.is_deleted == False))

            travel_type = db_session.execute(
                statement=query).scalar_one_or_none()

            # get departure and arrival locations
            query = select(LocationTable). \
                where(and_(LocationTable.id.in_(
                    [travel_detail.departure_location_id, travel_detail.arrival_location_id]),
                    LocationTable.is_deleted == False))

            locations = db_session.execute(statement=query).scalars().all()

            form.travel_type.data = travel_type.name
            form.departure_location.data = locations[0].name
            form.arrival_location.data = locations[1].name
            form.departure_time.data = travel_detail.departure_time.strftime("%Y-%m-%d %H:%M:%S")
            form.arrival_time.data = travel_detail.arrival_time.strftime("%Y-%m-%d %H:%M:%S")

            query = select(LocationTable)

            all_locations = db_session.execute(statement=query).scalars().all()

            query = select(TravelTypeTable)

            all_travel_type = db_session.execute(statement=query).scalars().all()

            response["travel_type"] = travel_type.name
            response["departure_locations"] = locations[0].name
            response["arrival_locations"] = locations[1].name
            response["departure_time"] = travel_detail.departure_time.strftime("%Y-%m-%d %H:%M:%S")
            response["arrival_time"] = travel_detail.arrival_time.strftime("%Y-%m-%d %H:%M:%S")
            response["all_locations"] = all_locations
            response["all_travel_type"] = all_travel_type

            return render_template("index.html", 
                form=form, 
                response=response,
                travel_types=[travel_type.name for travel_type in all_travel_type], 
                departure_locations=[location.name for location in all_locations],
                arrival_locations=[location.name for location in all_locations]
            )
        
        if request.method == "POST":
            form = UpdateBookingForm(request.form)
            
            # get location ids
            query = select(LocationTable). \
                where(and_(LocationTable.name.in_(
                    [form.departure_location.data, form.arrival_location.data]),
                    LocationTable.is_deleted == False))
            
            locations = db_session.execute(statement=query).scalars().all()

            # get travel type id
            query = select(TravelTypeTable).where(and_(TravelTypeTable.name == form.travel_type.data,
                                                    TravelTypeTable.is_deleted == False))
            
            travel_type = db_session.execute(
                statement=query).scalar_one_or_none()
            
            # get travel detail id
            query = select(TravelDetailTable).where(and_(TravelDetailTable.departure_location_id == locations[0].id,
                                                        TravelDetailTable.arrival_location_id == locations[1].id,
                                                        TravelDetailTable.departure_time == form.departure_time.data,
                                                        TravelDetailTable.arrival_time == form.arrival_time.data,
                                                        TravelDetailTable.travel_type_id == travel_type.id,
                                                        TravelDetailTable.is_deleted == False))
            
            travel_detail = db_session.execute(
                statement=query).scalar_one_or_none()
            
            if travel_detail is None:
                return ({"success": False, "message": "No travel available for given details", "data": None},
                        404, CONTENT_TYPE)
            
            # get expense
            query = select(ExpenseTable).where(and_(ExpenseTable.travel_detail_id == travel_detail.id,
                                                    ExpenseTable.is_deleted == False))
            
            expense = db_session.execute(statement=query).scalar_one_or_none()

            cost = expense.cost

            difference = (travel_detail.arrival_time - datetime.now()).days

            if difference > 80 and difference < 90:
                cost *= 0.8
            elif difference > 60 and difference < 80:
                cost *= 0.9
            elif difference > 46 and difference < 60:
                cost *= 0.95
            
            # get booking details
            query = select(BookingTable).where(and_(BookingTable.id == booking_id,
                                                    BookingTable.is_deleted == False))
            
            booking = db_session.execute(statement=query).scalar_one_or_none()

            if booking is None:
                return ({"success": False, "message": BOOKING_NOT_FOUND, "data": None},
                        404, CONTENT_TYPE)
            
            # update booking
            query = update(BookingTable).where(BookingTable.id == booking_id).values(
                travel_detail_id=travel_detail.id,
                cost=cost,
                status="success",
            )

            db_session.execute(statement=query)
            db_session.commit()

            return ({"success": True, "message": "Booking updated successfully", "data": None},
                    200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "booking already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid booking id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print(
            type(err).__name__,          # TypeError
            __file__,                  # /tmp/example.py
            err.__traceback__.tb_lineno  # 2
        )
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single booking route
@booking_router.delete("/<int:booking_id>/")
def delete_booking(
    booking_id: int, db_session: Session = get_session()
):
    """
        Delete a single booking.

        Description:
        - This method is used to delete a single booking by providing id.

        Parameters:
        - **booking_id** (INT): ID of booking to be deleted. *--Required*

        Returns:
        - **message** (STR): booking deleted successfully.

    """
    print("Calling delete_booking method")

    query = select(BookingTable).where(and_(BookingTable.id == booking_id,
                                            BookingTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": BOOKING_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "booking deleted successfully"},
            200, CONTENT_TYPE)


# Create a single booking by locations, type
@booking_router.post("/create/")
def create_booking_by_locations(
    db_session: Session = get_session()
):
    """
        Create a single booking by locations, type.

        Description:
        - This method is used to create a single booking.
        Parameters:
        - **travel_type** (STR): Type of travel. *--Required*
        - **departure_location** (STR): Departure location. *--Required*
        - **arrival_location** (STR): Arrival location. *--Required*
        - **user_id** (INT): Id of user. *--Optional*
        - **cost** (FLOAT): Cost of booking. *--Optional*

        Returns:
        Booking details along with following information:
        - **id** (INT): Id of booking.
        - **user_id** (INT): Id of user.
        - **travel_detail_id** (INT): Id of travel detail.
        - **cost** (FLOAT): Cost of booking.
        - **status** (ENUM): Status of booking.
        - **refund_amount** (FLOAT): Refund amount of booking.
        - **created_at** (DATETIME): Datetime of booking creation.
        - **updated_at** (DATETIME): Datetime of booking updation.

    """
    print("Calling create_booking_by_locations method")

    try:
        travel = {**request.json}

        query = select(TravelTypeTable).where(and_(TravelTypeTable.name == travel["travel_type"],
                                                   TravelTypeTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": "Invalid travel type", "data": None},
                    400, CONTENT_TYPE)

        travel["travel_type_id"] = result.id

        query = select(LocationTable).where(and_(LocationTable.name == travel["departure_location"],
                                                 LocationTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": "Invalid departure location", "data": None},
                    400, CONTENT_TYPE)

        travel["departure_location_id"] = result.id

        query = select(LocationTable).where(and_(LocationTable.name == travel["arrival_location"],
                                                 LocationTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": "Invalid arrival location", "data": None},
                    400, CONTENT_TYPE)

        travel["arrival_location_id"] = result.id

        query = select(TravelDetailTable).where(and_(TravelDetailTable.travel_type_id == travel["travel_type_id"],
                                                     TravelDetailTable.departure_location_id == travel[
                                                         "departure_location_id"],
                                                     TravelDetailTable.arrival_location_id == travel[
                                                         "arrival_location_id"],
                                                     TravelDetailTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": "Travel detail not found", "data": None},
                    400, CONTENT_TYPE)

        travel["travel_detail_id"] = result.id

        booking = BookingTable(user_id=travel.get("user_id"),
                               travel_detail_id=travel["travel_detail_id"],
                               cost=travel.get("cost"),
                               status="success",
                               refund_amount=0.0)

        db_session.add(booking)
        db_session.commit()

        return ({"success": True, "message": "Booking created successfully",
                 "data": booking.to_dict()}, 200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Booking already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid booking id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Cancel booking by id
@booking_router.get("/cancel/<int:booking_id>/")
def cancel_booking(
    booking_id: int, db_session: Session = get_session()
):
    """
        Cancel booking by id.

        Description:
        - This method is used to cancel booking by id.

        Parameters:
        - **booking_id** (INT): ID of booking to be cancelled. *--Required*

        Returns:
        - **message** (STR): booking cancelled successfully.

    """
    print("Calling cancel_booking method")

    query = select(BookingTable).where(and_(BookingTable.id == booking_id,
                                            BookingTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": BOOKING_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.status = "cancelled"

    time_difference = (datetime.now() - result.created_at).days

    if time_difference > 60:
        result.refund_amount = result.cost
    elif time_difference > 30:
        result.refund_amount = result.cost * 0.5
    else:
        result.refund_amount = 0.0

    db_session.commit()

    flash(message="Booking cancelled successfully", category="success")

    return redirect(url_for("dashboard.get_dashboard"))
