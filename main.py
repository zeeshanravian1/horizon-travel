"""
    Main file for project

    Description:
    - This program is main file for project.
    - It is used to create Flask object and add all routes to it.

"""

# Importing Python packages

# Importing Flask packages
from flask import Flask, render_template

# Importing from project files
from core import (CORS_ALLOW_HEADERS, CORS_ALLOW_METHODS, CORS_ALLOW_ORIGINS, PROJECT_TITLE)
from apps import (role_router, user_router)


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
    return render_template("index.html", message=f"Welcome to {PROJECT_TITLE}!")


# Register routers
app.register_blueprint(role_router)
app.register_blueprint(user_router)


# # Remove all code below this line when migrationg will be done
# from database import (metadata, get_session)
# from database.connection import (engine)
# from apps.role.model import (RoleTable)


# metadata.drop_all(bind=engine)
# metadata.create_all(bind=engine)


# def insert_roles(session = get_session()):
#     """
#         Insert roles

#         Description:
#         - This function is used to insert roles.

#         Parameters:
#         - **None**

#         Returns:
#         - **None**

#     """
#     print("Calling insert_roles method")


#     admin_role: RoleTable = RoleTable(role_name="admin")
#     user_role: RoleTable = RoleTable(role_name="user")

#     session.add(admin_role)
#     session.add(user_role)
#     session.commit()


# insert_roles()


# print("******************************************")
# print(app.url_map)
# print("******************************************")
