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
from apps.travel_type.model import (TravelTypeTable)
from apps.max_seat.model import (MaxSeatTable)
from .configuration import (ADMIN_NAME, ADMIN_CONTACT, ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
from .session import (get_session)


# --------------------------------------------------------------------------------------------------


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

    try:
        # Insert Admin
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

        # Insert locations
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

        # Insert price categories
        price_categories = ["business", "economic"]

        price_category_objects = [PriceCategoryTable(name=price_category)
                                  for price_category in price_categories]

        session.add_all(price_category_objects)
        session.commit()

        # Insert travel types
        travel_types = ["air", "train", "coach"]

        travel_type_objects = [TravelTypeTable(name=travel_type) for travel_type in travel_types]

        session.add_all(travel_type_objects)
        session.commit()

        # Insert max seats
        max_seats = [{"travel_type_id": 1, "seats": 120},
                     {"travel_type_id": 2, "seats": 300},
                     {"travel_type_id": 3, "seats": 50}]

        max_seat_objects = [MaxSeatTable(**max_seat) for max_seat in max_seats]

        session.add_all(max_seat_objects)
        session.commit()

    except Exception:
        pass
