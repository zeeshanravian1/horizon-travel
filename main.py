"""
    Main file for project

    Description:
    - This program is main file for project.
    - It is used to create Flask object and add all routes to it.

"""

# Importing Python packages

# Importing Flask packages
from flask import Flask

# Importing from project files
from core import (CORS_ALLOW_HEADERS, CORS_ALLOW_METHODS, CORS_ALLOW_ORIGINS, PROJECT_TITLE)
from apps import (user_router, auth_router)


# Flask object
app = Flask(__name__)


# --------------------------------------------------------------------------------------------------


# CORS
app.config["CORS_HEADERS"] = CORS_ALLOW_HEADERS
app.config["CORS_ORIGINS"] = CORS_ALLOW_ORIGINS
app.config["CORS_METHODS"] = CORS_ALLOW_METHODS


@app.route("/")
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

    return {"message": f"Welcome to {PROJECT_TITLE}!"}


# Register routers
app.register_blueprint(user_router)
app.register_blueprint(auth_router)


# print("******************************************")
# print(app.url_map)
# print("******************************************")
