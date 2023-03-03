"""
    User APIs Module

    Description:
    - This module is responsible for handling user APIs.
    - It is used to create, get, update, delete user details.

"""

# Importing Python packages
from sqlalchemy import (select, func, and_)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)
from passlib.hash import (pbkdf2_sha256)

# Importing Flask packages
from flask import (Blueprint, request, render_template, flash, redirect, url_for)
from flask_login import (login_required, current_user)

# Importing from project files
from database.session import (get_session)
from .exception import (USER_NOT_FOUND)
from .model import (UserTable)
from ..base import (CONTENT_TYPE)
from .form import (UpdateProfileForm)


user_router = Blueprint(
    name="UserRouter",
    import_name=__name__,
    url_prefix="/user",
)


# --------------------------------------------------------------------------------------------------


# Get a single user route
@user_router.get("/profile/")
@login_required
def get_user(
    db_session: Session = get_session()
):
    """
        Get a single user.

        Description:
        - This method is used to get a single user.

        Parameters:
        - **user_id** (INT): Id of user. *--Required*

        Returns:
        user details along with following information:
        - **id** (INT): Id of user.
        - **name** (STR): Name of user.
        - **contact** (STR): Contact of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **password** (STR): Password of user.
        - **is_admin** (BOOL): Is user admin or not.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

    """

    form = UpdateProfileForm()


    query = select(UserTable).where(and_(UserTable.id == current_user.id,
                                         UserTable.is_deleted == False))

    record = db_session.execute(statement=query).scalar_one_or_none()

    if record is None:
        return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    form.username.data = record.username
    form.name.data = record.name
    form.contact.data = record.contact
    form.email.data = record.email

    return render_template("profile.html", form=form, user=current_user)



# Get all users route
@user_router.get("/")
def get_all_users(
    page: int | None = None, limit: int | None = None,
    db_session: Session = get_session()
):
    """
        Get all users.

        Description:
        - This method is used to get all users.

        Parameters:
        - **page** (INT): Page number. *--Optional*
        - **limit** (INT): Limit of records per page. *--Optional*

        Returns:
        Get all users with following information:
        - **id** (INT): Id of user.
        - **name** (STR): Name of user.
        - **contact** (STR): Contact of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **password** (STR): Password of user.
        - **is_admin** (BOOL): Is user admin or not.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

    """

    query = select(func.count(UserTable.id)).where(UserTable.is_deleted == False)
    result = db_session.execute(query)
    total_count = result.scalar()

    query = select(UserTable).where(UserTable.is_deleted == False)

    if page and limit:
        query = select(UserTable).where(and_(
            UserTable.is_deleted == False, UserTable.id > (page - 1) * limit)).limit(limit)

    result = db_session.execute(query).scalars().all()

    if not result:
        return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)
    
    if not (page and limit):
        page = 1
        limit = total_count

    return ({"success": True, "message": "users fetched successfully",
             "data": {"total": total_count, "page": page, "limit": limit,
                      "items": [user.to_dict() for user in result]}},
            200, CONTENT_TYPE)


# Update a single user route
@user_router.route("/update/", methods=["POST"])
@login_required
def update_user(
    db_session: Session = get_session()
):
    """
        Update a single user.

        Description:
        - This method is used to update a single user by providing id.

        Parameters:
        - **user_id** (INT): Id of user. *--Required*
        - **name** (STR): Name of user. *--Optional*
        - **contact** (STR): Contact of user. *--Optional*
        - **username** (STR): Username of user. *--Optional*
        - **email** (STR): Email of user. *--Optional*
        - **password** (STR): Password of user. *--Optional*

        Returns:
        user details along with following information:
        - **id** (INT): Id of user.
        - **name** (STR): Name of user.
        - **contact** (STR): Contact of user.
        - **username** (STR): Username of user.
        - **email** (STR): Email of user.
        - **password** (STR): Password of user.
        - **is_admin** (BOOL): Is user admin or not.
        - **created_at** (DATETIME): Datetime of user creation.
        - **updated_at** (DATETIME): Datetime of user updation.

    """

    try:

        form = UpdateProfileForm()

        query = select(UserTable).where(and_(UserTable.id == current_user.id,
                                             UserTable.is_deleted == False))

        result = db_session.execute(query).scalar_one_or_none()

        if result is None:
            return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                    404, CONTENT_TYPE)

        result.name = form.name.data
        result.contact = form.contact.data
        result.username = form.username.data
        result.email = form.email.data
        if form.password.data:
            result.password = pbkdf2_sha256.hash(form.password.data)

        db_session.add(result)
        db_session.commit()

        flash("Profile updated successfully", "success")
        return redirect(url_for("HomePage.get_homepage"))

    except IntegrityError as err:
        db_session.rollback()
        if err.orig.args[0] == 1062:
            return ({"success": False, "message": "user already exists", "data": None},
                    409, CONTENT_TYPE)

        if err.orig.args[0] == 1452:
            return ({"success": False, "message": "Invalid user id", "data": None},
                    400, CONTENT_TYPE)

        return ({"success": False, "message": "Integrity error", "data": None},
                400, CONTENT_TYPE)

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Internal server error", "data": None},
                500, CONTENT_TYPE)
    
    finally:
        db_session.close()


# Delete a single user route
@user_router.delete("/<int:user_id>/")
def delete_user(
    user_id: int, db_session: Session = get_session()
):
    """
        Delete a single user.

        Description:
        - This method is used to delete a single user by providing id.

        Parameters:
        - **user_id** (INT): ID of user to be deleted. *--Required*

        Returns:
        - **message** (STR): User deleted successfully.

    """

    query = select(UserTable).where(and_(UserTable.id == user_id,
                                         UserTable.is_deleted == False))

    result = db_session.execute(query).scalar_one_or_none()

    if result is None:
        return ({"success": False, "message": USER_NOT_FOUND, "data": None},
                404, CONTENT_TYPE)

    result.is_deleted = True

    db_session.commit()

    return ({"success": True, "message": "User deleted successfully"},
            200, CONTENT_TYPE)
