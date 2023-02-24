"""
    Database Initialization

    Description:
    - This module is responsible for initializing database.

"""

# Importing Python packages
from passlib.hash import (pbkdf2_sha256)

# Importing FastAPI packages

# Importing from project files
from apps.user.model import (UserTable)
from apps.location.model import (LocationTable)
from apps.price_category.model import (PriceCategoryTable)
from .configuration import (ADMIN_NAME, ADMIN_CONTACT, ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
from .session import (get_session)


# --------------------------------------------------------------------------------------------------


def insert_admin(session):
    """
        Insert admin

        Description:
        - This function is used to insert admin.

        Parameters:
        - **None**

        Returns:
        - **None**

    """
    print("Calling insert_admin method")

    try:
        admin: UserTable = UserTable(
            name=ADMIN_NAME,
            contact=ADMIN_CONTACT,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=pbkdf2_sha256.hash(ADMIN_PASSWORD),
            is_admin=True
        )

        session.add(admin)
        session.commit()

    except Exception:
        pass


# Insert Locations
def insert_locations(session):
    """
        Insert locations

        Description:
        - This function is used to insert locations.

        Parameters:
        - **None**

        Returns:
        - **None**

    """
    print("Calling insert_locations method")

    try:
        locations = [{"name": "Aberdeen", "latitude": 57.1482436, "longitude": -2.0928095},
                     {"name": "Birmingham", "latitude": 52.4796992, "longitude": -1.9026911},
                     {"name": "Bristol", "latitude": 51.4538022, "longitude": -2.5972985},
                     {"name": "Cardiff", "latitude": 51.4816546, "longitude": -3.1791934},
                     {"name": "Dundee", "latitude": 56.4614281, "longitude": -2.9681009},
                     {"name": "Edinburgh", "latitude": 55.9533456, "longitude": -3.1883749},
                     {"name": "Glasgow", "latitude": 55.861138, "longitude": -4.250196},
                     {"name": "London", "latitude": 51.5073219, "longitude": -0.1276474},
                     {"name": "Manchester", "latitude": 53.4794892, "longitude": -2.2451148},
                     {"name": "Newcastle", "latitude": 54.9748484, "longitude": -1.6140793},
                     {"name": "Portsmouth", "latitude": 50.7989132, "longitude": -1.0911629},
                     {"name": "Southampton", "latitude": 50.9025349, "longitude": -1.404189}]

        location_objects = [LocationTable(**location)
                            for location in locations]

        session.add_all(location_objects)
        session.commit()

    except Exception:
        pass


# Insert price categories
def insert_price_categories(session):
    """
        Insert price categories

        Description:
        - This function is used to insert price categories.

        Parameters:
        - **None**

        Returns:
        - **None**

    """
    print("Calling insert_price_categories method")

    try:
        price_categories = ["business", "economic"]

        price_category_objects = [PriceCategoryTable(name=price_category)
                                  for price_category in price_categories]

        session.add_all(price_category_objects)
        session.commit()

    except Exception:
        pass


# Insert Data
def insert_data(session=get_session()):
    """
        Insert data

        Description:
        - This function is used to insert data.

        Parameters:
        - **None**

        Returns:
        - **None**

    """
    print("Calling insert_data method")

    insert_admin(session)
    insert_locations(session)
    insert_price_categories(session)
