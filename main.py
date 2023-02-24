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
from apps import (auth_router, location_router, price_category_router, user_router)


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
app.register_blueprint(location_router)
app.register_blueprint(price_category_router)
app.register_blueprint(user_router)


# print("******************************************")
# print(app.url_map)
# print("******************************************")
