"""
    Expense APIs Module

    Description:
    - This module is responsible for handling expense APIs.
    - It is used to create, get, update, delete expense details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from flask import (Blueprint, request)

# Importing from project files
from database.session import (get_session)
from .exception import (EXPENSE_NOT_FOUND)
from .model import (ExpenseTable)
from ..base import (CONTENT_TYPE)


expense_router = Blueprint(
    name="ExpenseRouter",
    import_name=__name__,
    url_prefix="/expense",
)


# --------------------------------------------------------------------------------------------------


# Create a single expense
@expense_router.post("/")
def create_expense(
    db_session: Session = get_session()
):
    """
        Create a single expense.

        Description:
        - This method is used to create a single expense.

        Parameters:
        expense details to be created with following fields:
        - **travel_detail_id** (INT): Id of travel detail. *--Required*
        - **price_category_id** (INT): Id of price category. *--Required*
        - **cost** (FLOAT): Cost of expense. *--Required*

        Returns:
        expense details along with following information:
        - **id** (INT): Id of expense.
        - **travel_detail_id** (INT): Id of travel detail.
        - **price_category_id** (INT): Id of price category.
        - **cost** (FLOAT): Cost of expense.
        - **created_at** (DATETIME): Datetime of expense creation.
        - **updated_at** (DATETIME): Datetime of expense updation.
    """
    print("Calling create_expense method")

    try:
        record = ExpenseTable(**request.json)

        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        return ({"success": True, "message": "Expense created successfully",
                 "data": record.to_dict()}, 201, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Expense already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid expense id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": None},
                500, CONTENT_TYPE)


# Get a single expense route
@expense_router.get("/<int:expense_id>/")
def get_expense(
    expense_id: int, db_session: Session = get_session()
):
    """
        Get a single expense.

        Description:
        - This method is used to get a single expense.

        Parameters:
        - **expense_id** (INT): Id of expense. *--Required*

        Returns:
        expense details along with following information:
        - **id** (INT): Id of expense.
        - **travel_detail_id** (INT): Id of travel detail.
        - **price_category_id** (INT): Id of price category.
        - **cost** (FLOAT): Cost of expense.
        - **created_at** (DATETIME): Datetime of expense creation.
        - **updated_at** (DATETIME): Datetime of expense updation.

    """
    print("Calling get_expense method")

    query = select(ExpenseTable).where(and_(ExpenseTable.id == expense_id,
                                             ExpenseTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": EXPENSE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    return ({"success": True, "message": "expense fetched successfully", "data": record.to_dict()},
            200, CONTENT_TYPE)


# Get all expenses route
@expense_router.get("/")
def get_all_expenses(
    page: int | None = None, limit: int | None = None,
    db_session: Session = get_session()
):
    """
        Get all expenses.

        Description:
        - This method is used to get all expenses.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all expenses with following information:
        - **id** (INT): Id of expense.
        - **travel_detail_id** (INT): Id of travel detail.
        - **price_category_id** (INT): Id of price category.
        - **cost** (FLOAT): Cost of expense.
        - **created_at** (DATETIME): Datetime of expense creation.
        - **updated_at** (DATETIME): Datetime of expense updation.

    """
    print("Calling get_all_expenses method")

    query = select(func.count(ExpenseTable.id)).where(
        ExpenseTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(ExpenseTable).where(ExpenseTable.is_deleted == False)

    if page and limit:
        query = select(ExpenseTable).where(and_(
            ExpenseTable.is_deleted == False, ExpenseTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": EXPENSE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)
    
    if not (page and limit):
        page = 1
        limit = total_count

    return ({"success": True, "message": "expenses fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [expense.to_dict() for expense in result]}},
            200, CONTENT_TYPE)


# Update a single expense route
@expense_router.put("/<int:expense_id>/")
def update_expense(
    expense_id: int, db_session: Session = get_session()
):
    """
        Update a single expense.

        Description:
        - This method is used to update a single expense by providing id.

        Parameters:
        - **expense_id** (INT): Id of expense. *--Required*
        - **travel_detail_id** (INT): Id of travel detail. *--Optional*
        - **price_category_id** (INT): Id of price category. *--Optional*
        - **cost** (FLOAT): Cost of expense. *--Optional*

        Returns:
        expense details along with following information:
        - **id** (INT): Id of expense.
        - **travel_detail_id** (INT): Id of travel detail.
        - **price_category_id** (INT): Id of price category.
        - **cost** (FLOAT): Cost of expense.
        - **created_at** (DATETIME): Datetime of expense creation.
        - **updated_at** (DATETIME): Datetime of expense updation.

    """
    print("Calling update_expense method")

    try:
        query = select(ExpenseTable).where(and_(ExpenseTable.id == expense_id,
                                                 ExpenseTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": EXPENSE_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)
        
        if result.name == request.json["name"]:
            return ({"success": False, "message": "expense already exists", "data": None},
                    409, CONTENT_TYPE)

        result.travel_detail_id = request.json.get("travel_detail_id", result.travel_detail_id)
        result.price_category_id = request.json.get("price_category_id", result.price_category_id)
        result.cost = request.json.get("cost", result.cost)

        db_session.commit()

        return ({"success": True, "message": "Expense updated successfully", "data": result.to_dict()},
                200, CONTENT_TYPE)

    except IntegrityError as err:
        print("integrity error", err)
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "Expense already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid expense id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)


# Delete a single expense route
@expense_router.delete("/<int:expense_id>/")
def delete_expense(
    expense_id: int, db_session: Session = get_session()
):
    """
        Delete a single expense.

        Description:
        - This method is used to delete a single expense by providing id.

        Parameters:
        - **expense_id** (INT): ID of expense to be deleted. *--Required*

        Returns:
        - **message** (STR): expense deleted successfully.

    """
    print("Calling delete_expense method")

    query = select(ExpenseTable).where(and_(ExpenseTable.id == expense_id,
                                             ExpenseTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": EXPENSE_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "expense deleted successfully"},
            200, CONTENT_TYPE)
