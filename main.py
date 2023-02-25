"""
    Main file for project

    Description:
    - This program is main file for project.
    - It is used to create Flask object and add all routes to it.

"""

# Importing Python packages
import os

# Importing Flask packages
from flask import (render_template)
from wsgi import app
from flask_login import login_required

# Importing from project files
from core import (CORS_ALLOW_HEADERS, CORS_ALLOW_METHODS, CORS_ALLOW_ORIGINS, PROJECT_TITLE)
from apps import (auth_router, booking_router, expense_router, location_router, max_seat_router,
                  price_category_router, travel_detail_router, travel_type_router, user_router,
                  homepage_router, records_router)


# Flask object


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# --------------------------------------------------------------------------------------------------


# CORS
app.config["CORS_HEADERS"] = CORS_ALLOW_HEADERS
app.config["CORS_ORIGINS"] = CORS_ALLOW_ORIGINS
app.config["CORS_METHODS"] = CORS_ALLOW_METHODS


@app.route("/")
@login_required
def root():
    """
        Root

        Description:
        - This function is used to create the root route.

        Parameters:
        - **None**

        Returns:
        - **None

    """

    return render_template("index.html", title=PROJECT_TITLE)


# Register routers
app.register_blueprint(auth_router)
app.register_blueprint(booking_router)
app.register_blueprint(expense_router)
app.register_blueprint(location_router)
app.register_blueprint(max_seat_router)
app.register_blueprint(price_category_router)
app.register_blueprint(travel_detail_router)
app.register_blueprint(travel_type_router)
app.register_blueprint(user_router)
app.register_blueprint(homepage_router)
app.register_blueprint(records_router)
