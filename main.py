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


# # Remove all code below this line when migrationg will be done
# from database import (metadata, get_session)
# from database.connection import (engine)
# from apps.user.model import (UserTable)
# from passlib.hash import (pbkdf2_sha256)
# import environs


# metadata.drop_all(bind=engine)
# metadata.create_all(bind=engine)


# env = environs.Env()

# # Admin
# NAME: str = env.str("ADMIN_NAME")
# CONTACT: str = env.str("ADMIN_CONTACT")
# USERNAME: str = env.str("ADMIN_USERNAME")
# EMAIL: str = env.str("ADMIN_EMAIL")
# PASSWORD: str = env.str("ADMIN_PASSWORD")


# def insert_admin(session = get_session()):
#     """
#         Insert admin

#         Description:
#         - This function is used to insert admin.

#         Parameters:
#         - **None**

#         Returns:
#         - **None**

#     """
#     print("Calling insert_admin method")

#     admin: UserTable = UserTable(
#         name=NAME,
#         contact=CONTACT,
#         username=USERNAME,
#         email=EMAIL,
#         password=pbkdf2_sha256.hash(PASSWORD),
#         is_admin=True
#     )
    
#     session.add(admin)
#     session.commit()


# insert_admin()


# print("******************************************")
# print(app.url_map)
# print("******************************************")
