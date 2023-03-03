"""
    Authentication Module

    Description:
    - This module is responsible for handling authentication APIs.

"""

# Importing Python packages
from passlib.hash import (pbkdf2_sha256)
from sqlalchemy import (select)
from sqlalchemy.orm import (Session)
from sqlalchemy.exc import (IntegrityError, PendingRollbackError, InvalidRequestError,
                            StatementError, ResourceClosedError)

# Importing Flask packages
from flask import (Blueprint, flash, request, render_template, redirect, url_for)
from flask_login import (login_user, logout_user, login_required, current_user)
from wsgi import (login_manager)


# Importing from project files
from database.session import (get_session)
from .exception import (PASSWORD_INCORRECT)
from .form import (LoginForm, RegistrationForm)
from ..user.model import (UserTable)
from apps.booking.model import (BookingTable)


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
        - **None**

        Returns:
        - **None**

    """

    try:
        register_form = RegistrationForm()

        if request.method == "GET":
            return render_template("register.html", form=register_form)

        if not register_form.validate_on_submit():
            flash("Please fill all the fields.", "error")
            return render_template("register.html", form=register_form)


        # Creating user data
        user_data: UserTable = UserTable(
            name=register_form.name.data,
            contact=register_form.contact.data,
            username=register_form.username.data,
            email=register_form.email.data,
            password=pbkdf2_sha256.hash(register_form.password.data),
            is_admin=False,
        )

        # Adding user data to database
        db_session.add(user_data)
        db_session.commit()
        db_session.refresh(user_data)

        booking_id = request.args.get("booking_id", None)

        if booking_id:
            booking = db_session.query(BookingTable).filter_by(id=booking_id).first()
            booking.user_id = user_data.id
            db_session.commit()

        flash("Registered successfully.", "success")
        return redirect(url_for("AuthenticationRouter.login"))

    except (IntegrityError, PendingRollbackError, InvalidRequestError,
            StatementError, ResourceClosedError) as err:
        db_session.rollback()
        flash("Username or email already exists.")
        return render_template("register.html", form=register_form)

    except Exception as err:
        db_session.rollback()
        flash("Something went wrong.")
        return render_template("register.html", form=register_form)

# Login Route
@auth_router.route("/login", methods=["GET", "POST"])
def login(db_session: Session = get_session()):
    """
        Login Route

        Description:
        - This route is responsible for handling login requests.

        Parameters:
        - **None**

        Returns:
        - **None**

    """

    if current_user.is_authenticated:
        return redirect(url_for("root"))

    login_form = LoginForm()

    if request.method == "GET":
        return render_template("login.html", form=login_form)

    if not login_form.validate_on_submit():
        flash("Invalid credentials.", "error")
        return render_template("login.html", form=login_form)

    # Getting user data
    query = select(UserTable).where(UserTable.email == login_form.email.data)
    user_data = db_session.execute(query).scalar_one_or_none()

    if not user_data:
        flash('User not found!', 'error')
        return render_template("login.html", form=login_form)

    if not pbkdf2_sha256.verify(login_form.password.data, user_data.password):
        flash(PASSWORD_INCORRECT, 'error')
        return render_template("login.html", form=login_form)
    
    booking_id = request.args.get("booking_id", None)

    if booking_id:
        booking = db_session.query(BookingTable).filter_by(id=booking_id).first()
        booking.user_id = user_data.id
        db_session.commit()

    flash("Logged in successfully.", 'success')
    login_user(user_data, remember=login_form.remember.data)
    return redirect(url_for("HomePage.get_homepage"))


# Logout Route
@auth_router.route("/logout", methods=["GET"])
@login_required
def logout():
    """
        Logout Route

        Description:
        - This route is responsible for handling logout requests.

        Parameters:
        - **None**

        Returns:
        - **None**

    """

    logout_user()
    flash("Logged out successfully.", "success")

    return redirect(url_for("AuthenticationRouter.login"))


@login_manager.unauthorized_handler
def unauthorized():
    """
        Unauthorized Handler

        Description:
        - This handler is responsible for handling unauthorized requests.

        Parameters:
        - **None**

        Returns:
        - **None**

    """

    return redirect(location=url_for("AuthenticationRouter.login"))
