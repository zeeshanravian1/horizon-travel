"""
    Authentication Module

    Description:
    - This module is responsible for handling authentication APIs.

"""

# Importing Python packages
from passlib.hash import (pbkdf2_sha256)
from sqlalchemy import (select)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError)

# Importing Flask packages
from wsgi import (login_manager)
from flask import (Blueprint, flash, request, render_template, redirect, url_for)
from flask_login import (login_user, logout_user, login_required)

# Importing from project files
from database.session import (get_session)
from .exception import (DISABLE_USER, USER_NOT_FOUND, PASSWORD_INCORRECT)
from .form import (LoginForm, RegistrationForm)
from ..base import (CONTENT_TYPE)
from ..user.model import (UserTable)


auth_router = Blueprint(
    name="AuthenticationRouter",
    import_name=__name__,
    url_prefix="/auth",
)


# --------------------------------------------------------------------------------------------------


# Registration Route
@auth_router.route("/register", methods=["GET", "POST"])
def register(db_session: Session = get_session()):
    """
        Registration Route

        Description:
        - This route is responsible for handling registration requests.

        Parameters:
        - None

        Returns:
        - None

    """
    print("Calling registration route")

    register_form = RegistrationForm()

    if request.method == "GET":
        return render_template("register.html", form=register_form)

    # Creating user data
    user_data = UserTable(
        name=register_form.name.data,
        contact=register_form.contact.data,
        username=register_form.username.data,
        email=register_form.email.data,
        password=pbkdf2_sha256.hash(register_form.password.data),
        is_admin=False,
    )

    # Adding user data to database
    db_session.add(user_data)

    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        flash("Username or email already exists.")
        return ({"success": False, "message": "Username or email already exists.", "data": None},
                400, CONTENT_TYPE)

    flash("Registered successfully.")

    return ({"success": True, "message": "Registered successfully.", "data": None},
            200, CONTENT_TYPE)


# Login Route
@auth_router.route("/login", methods=["GET", "POST"])
def login(db_session: Session = get_session()):
    """
        Login Route

        Description:
        - This route is responsible for handling login requests.

        Parameters:
        - None

        Returns:
        - None

    """
    print("Calling login route")

    login_form = LoginForm()

    if request.method == "GET":
        return render_template("login.html", form=login_form)

    if not login_form.validate_on_submit():
        return render_template("login.html", form=login_form)

    print(login_form.email.data, login_form.password.data)
    # Getting user data
    query = select(UserTable).where(UserTable.email == login_form.email.data)
    user_data = db_session.execute(query).scalar_one_or_none()
    print(user_data)
    if not user_data:
        flash('User not found!', 'error')
        return render_template("login.html", form=login_form)


    if not pbkdf2_sha256.verify(login_form.password.data, user_data.password):
        flash(PASSWORD_INCORRECT, 'error')
        return render_template("login.html", form=login_form)

    flash("Logged in successfully.", 'success')
    login_user(user_data, remember=login_form.remember.data)
    return redirect(url_for("root"))


# Logout Route
@auth_router.route("/logout", methods=["GET"])
@login_required
def logout():
    """
        Logout Route

        Description:
        - This route is responsible for handling logout requests.

        Parameters:
        - None

        Returns:
        - None

    """
    print("Calling logout route")

    logout_user()
    flash("Logged out successfully.")

    return redirect(url_for("AuthenticationRouter.login"))

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(location=url_for("AuthenticationRouter.login"))