"""
    Travel Detail APIs Module

    Description:
    - This module is responsible for handling travel detail APIs.
    - It is used to create, get, update, delete travel detail details.

"""

# Importing Python packages
from sqlalchemy import (select, update, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request, flash, render_template, redirect, url_for)
from flask_login import (login_required, current_user)

# Importing from project files
from database.session import (get_session)
from .exception import (TRAVEL_DETAIL_NOT_FOUND)
from .model import (TravelDetailTable)
from apps.location.model import (LocationTable)
from apps.travel_type.model import (TravelTypeTable)
from apps.expense.model import (ExpenseTable)
from apps.price_category.model import (PriceCategoryTable)
from ..base import (CONTENT_TYPE)
from .form import (TravelDetailForm)


travel_detail_router = Blueprint(
    name="TravelDetailRouter",
    import_name=__name__,
    url_prefix="/travel_detail",
)


# --------------------------------------------------------------------------------------------------


# Create a single travel detail
@travel_detail_router.route("/create/", methods=["GET", "POST"])
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
        if request.method == "GET":
            response = {}
            
            # get all locations
            query = select(LocationTable).where(LocationTable.is_deleted == False)

            locations = db_session.execute(statement=query).scalars().all()
            locations = [{"id": location.id, "name": location.name} for location in locations]

            response["locations"] = locations

            # get all travel types
            query = select(TravelTypeTable).where(TravelTypeTable.is_deleted == False)

            travel_types = db_session.execute(statement=query).scalars().all()
            travel_types = [{"id": travel_type.id, "name": travel_type.name} for travel_type in travel_types]

            response["travel_types"] = travel_types

            return render_template("newtravels.html", response=response, create_travel=True)

        else:
            print(
                request.form.get("departure_location"),
                request.form.get("arrival_location"),
                request.form.get("travel_type"),
                request.form.get("departure_time"),
                request.form.get("arrival_time"),
                request.form.get("expense")
            )
        # get location ids
        query = select(LocationTable). \
            where(and_(LocationTable.name.in_(
                [request.form.get("departure_location"),
                    request.form.get("arrival_location")]),
                LocationTable.is_deleted == False))

        locations = db_session.execute(statement=query).scalars().all()

        # get travel type id
        query = select(TravelTypeTable).where(and_(TravelTypeTable.name == form.travel_type.data,
                                                    TravelTypeTable.is_deleted == False))

        travel_type = db_session.execute(
            statement=query).scalar_one_or_none()
        
        record = TravelDetailTable(
            travel_type_id=travel_type.id,
            departure_location_id=locations[0].id,
            departure_time=form.departure_time.data,
            arrival_location_id=locations[1].id,
            arrival_time=form.arrival_time.data
        )

        db_session.add(record)
        db_session.commit()

        # get inserted record
        query = select(TravelDetailTable).where(and_(TravelDetailTable.id == record.id,
                                                    TravelDetailTable.is_deleted == False))
        
        record = db_session.execute(statement=query).scalar_one_or_none()

        expense_record = ExpenseTable(
            travel_detail_id=record.id,
            amount=request.form.get("cost")
        )

        db_session.add(expense_record)
        db_session.commit()

        return ({"success": True, "message": "Travel detail created successfully"},
                201, CONTENT_TYPE)

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
        raise err
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# # Get a single travel detail route
# @travel_detail_router.get("/<int:travel_detail_id>/")
# def get_travel_detail(
#     travel_detail_id: int, db_session: Session = get_session()
# ):
#     """
#         Get a single travel detail.

#         Description:
#         - This method is used to get a single travel detail.

#         Parameters:
#         - **travel_detail_id** (INT): Id of travel detail. *--Required*

#         Returns:
#         travel detail details along with following information:
#         - **id** (INT): Id of travel detail.
#         - **travel_type_id** (INT): Id of travel type.
#         - **departure_location_id** (INT): Id of departure location.
#         - **departure_time** (DATETIME): Datetime of departure.
#         - **arrival_location_id** (INT): Id of arrival location.
#         - **arrival_time** (DATETIME): Datetime of arrival.
#         - **created_at** (DATETIME): Datetime of travel detail creation.
#         - **updated_at** (DATETIME): Datetime of travel detail updation.

#     """

#     query = select(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
#                                                TravelDetailTable.is_deleted == False))

#     record = db_session.execute(statement=query).scalar_one_or_none()

#     if record is None:
#         return ({"success": False, "message": TRAVEL_DETAIL_NOT_FOUND, "data": None},
#                 404, CONTENT_TYPE)

#     return ({"success": True, "message": "Travel detail fetched successfully", "data": record.to_dict()},
#             200, CONTENT_TYPE)


# Get all travel details route
@travel_detail_router.route("/all/", methods=["GET"])
def get_all_travel_categories(
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

    response = []

    query = select(func.count(TravelDetailTable.id)).where(
        TravelDetailTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(TravelDetailTable).where(TravelDetailTable.is_deleted == False)

    travel_details = db_session.execute(query).scalars().all()

    for travel_detail in travel_details:
        travel_detail = travel_detail.to_dict()
        travel_type = db_session.query(TravelTypeTable).filter(
            TravelTypeTable.id == travel_detail["travel_type_id"]).first()
        
        travel_detail["travel_type"] = travel_type.name

        departure_location = db_session.query(LocationTable).filter(
            LocationTable.id == travel_detail["departure_location_id"]).first()
        
        travel_detail["departure_location"] = departure_location.name

        arrival_location = db_session.query(LocationTable).filter(
            LocationTable.id == travel_detail["arrival_location_id"]).first()
        
        travel_detail["arrival_location"] = arrival_location.name

        travel_detail["arrival_location"] = arrival_location.name

        expense = db_session.query(ExpenseTable).filter(
            ExpenseTable.travel_detail_id == travel_detail["id"]).all()

        for expense in expense:
            data = travel_detail.copy()
            query = select(PriceCategoryTable).where(
                PriceCategoryTable.id == expense.price_category_id)
            price_category = db_session.execute(query).scalar_one_or_none()

            data["class_type"] = price_category.name

            data["expense"] = expense.cost

            del data["travel_type_id"]
            del data["departure_location_id"]
            del data["arrival_location_id"]
            del data["is_deleted"]
            del data["created_at"]
            del data["updated_at"]

            response.append(data)

    return render_template("travels.html", travel_detail=response)

# Update a single travel detail route
@travel_detail_router.route("/update/<int:travel_detail_id>/", methods=["GET", "POST"])
@login_required
def update_travel_detail(
    travel_detail_id: int = 0, db_session: Session = get_session()
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
        if not current_user.is_admin:
            return ({"success": False, "message": "You are not authorized to perform this action", "data": None},
                    401, CONTENT_TYPE)

        if request.method == "GET":
            response = {}
            form = TravelDetailForm(request.form)

            query = select(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
                                                            TravelDetailTable.is_deleted == False))

            travel_detail = db_session.execute(query).scalar_one_or_none()

            if travel_detail is None:
                flash(TRAVEL_DETAIL_NOT_FOUND, "error")
                return redirect(url_for("travel_detail.get_all_travel_categories", travel_detail_id=travel_detail_id))
            
            query = select(TravelTypeTable).where(TravelTypeTable.id == travel_detail.travel_type_id)
            travel_type = db_session.execute(statement=query).scalar_one_or_none()

            query = select(LocationTable).where(LocationTable.id == travel_detail.departure_location_id)
            departure_location = db_session.execute(statement=query).scalar_one_or_none()

            query = select(LocationTable).where(LocationTable.id == travel_detail.arrival_location_id)
            arrival_location = db_session.execute(statement=query).scalar_one_or_none()

            expense = db_session.query(ExpenseTable).filter(
            ExpenseTable.travel_detail_id == travel_detail.id).first()

            form.departure_location.data = departure_location.name
            form.arrival_location.data = arrival_location.name
            form.travel_type.data = travel_type.name
            form.departure_time.data = travel_detail.departure_time
            form.arrival_time.data = travel_detail.arrival_time
            form.expense.data = expense.cost

            response["id"] = travel_detail.id
            response["departure_location"] = departure_location.name
            response["arrival_location"] = arrival_location.name
            response["travel_type"] = travel_type.name
            response["departure_time"] = travel_detail.departure_time
            response["arrival_time"] = travel_detail.arrival_time
            response["expense"] = expense.cost

            # get all locations
            query = select(LocationTable).where(LocationTable.is_deleted == False)

            locations = db_session.execute(statement=query).scalars().all()
            locations = [{"id": location.id, "name": location.name} for location in locations]

            response["locations"] = locations

            # get all travel types
            query = select(TravelTypeTable).where(TravelTypeTable.is_deleted == False)

            travel_types = db_session.execute(statement=query).scalars().all()
            travel_types = [{"id": travel_type.id, "name": travel_type.name} for travel_type in travel_types]

            response["travel_types"] = travel_types
            
            return render_template("newtravels.html", form=form, response=response, travel_detail_id=travel_detail_id)
        
        if request.method == "POST":
            # form = TravelDetailForm(request.form)
            print(
                request.form.get("departure_location"),
                request.form.get("arrival_location"),
                request.form.get("travel_type"),
                request.form.get("departure_time"),
                request.form.get("arrival_time"),
                request.form.get("expense")
            )
            # get location ids
            query = select(LocationTable). \
                where(and_(LocationTable.name.in_(
                    [request.form.get("departure_location"),
                     request.form.get("arrival_location")]),
                    LocationTable.is_deleted == False))

            locations = db_session.execute(statement=query).scalars().all()

            # get travel type id
            query = select(TravelTypeTable).where(and_(TravelTypeTable.name == form.travel_type.data,
                                                       TravelTypeTable.is_deleted == False))

            travel_type = db_session.execute(
                statement=query).scalar_one_or_none()
            
            
            query = update(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
                                                            TravelDetailTable.is_deleted == False)). \
                    values(travel_type_id=travel_type.id,
                        departure_location_id=locations[0].id,
                        departure_time=form.departure_time.data,
                        arrival_location_id=locations[1].id,
                        arrival_time=form.arrival_time.data)
            
            db_session.execute(query)
            db_session.commit()

            # update expense
            query = update(ExpenseTable).where(and_(ExpenseTable.travel_detail_id == travel_detail_id,
                                                    ExpenseTable.is_deleted == False)). \
                    values(cost=form.expense.data)
            
            db_session.execute(query)
            db_session.commit()

            return ({"success": True, "message": "Travel detail updated successfully",
                     "data": None}, 200, CONTENT_TYPE)


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
        print(
            type(err).__name__,          # TypeError
            __file__,                  # /tmp/example.py
            err.__traceback__.tb_lineno  # 2
        )
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single travel detail route
@travel_detail_router.route("/delete/<int:travel_detail_id>/")
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
    try:
        query = select(TravelDetailTable).where(and_(TravelDetailTable.id == travel_detail_id,
                                                TravelDetailTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": TRAVEL_DETAIL_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        result.is_deleted = True

        db_session.commit()

        flash(message="Travel detail deleted successfully", category="success")
        return redirect(url_for("TravelDetailRouter.get_all_travel_categories"))
    
    except Exception as err:
        print(
            type(err).__name__,          # TypeError
            __file__,                  # /tmp/example.py
            err.__traceback__.tb_lineno  # 2
        )
        db_session.rollback()
        return redirect(url_for("TravelDetailRouter.get_all_travel_categories"))
    
    finally:
        db_session.close()
