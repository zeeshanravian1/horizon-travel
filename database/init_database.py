"""
    Database Initialization

    Description:
    - This module is responsible for initializing database.

"""

# Importing Python packages
from datetime import (datetime, timedelta)
from passlib.hash import (pbkdf2_sha256)

# Importing FastAPI packages

# Importing from project files
from apps.user.model import (UserTable)
from apps.location.model import (LocationTable)
from apps.price_category.model import (PriceCategoryTable)
from apps.travel_type.model import (TravelTypeTable)
from apps.max_seat.model import (MaxSeatTable)
from apps.travel_detail.model import (TravelDetailTable)
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

        # Insert travel details
        locations = session.query(LocationTable).all()
        locations = {location.name: location.id for location in locations}

        travel_details = [
            {
                "departure_location": "Newcastle",
                "departure_time": "2022-10-23 16:45:00",
                "arrival_location": "Bristol",
                "arrival_time": "2022-10-23 18:00:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "2022-10-23 08:00:00",
                "arrival_location": "Newcastle",
                "arrival_time": "2022-10-23 09:15:00"
            },
            {
                "departure_location": "Cardiff",
                "departure_time": "2022-10-23 06:00:00",
                "arrival_location": "Edinburgh",
                "arrival_time": "2022-10-23 07:30:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "2022-10-23 11:30:00",
                "arrival_location": "Manchester",
                "arrival_time": "2022-10-23 12:30:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "2022-10-23 12:20:00",
                "arrival_location": "Bristol",
                "arrival_time": "2022-10-23 13:20:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "2022-10-23 07:40:00",
                "arrival_location": "London",
                "arrival_time": "2022-10-23 08:20:00"
            },
            {
                "departure_location": "London",
                "departure_time": "2022-10-23 11:00:00",
                "arrival_location": "Manchester",
                "arrival_time": "2022-10-23 12:20:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "2022-10-23 12:20:00",
                "arrival_location": "Glasgow",
                "arrival_time": "2022-10-23 13:30:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "2022-10-23 07:40:00",
                "arrival_location": "Glasgow",
                "arrival_time": "2022-10-23 08:45:00"
            },
            {
                "departure_location": "Glasgow",
                "departure_time": "2022-10-23 14:30:00",
                "arrival_location": "Newcastle",
                "arrival_time": "2022-10-23 15:45:00"
            },
            {
                "departure_location": "Newcastle",
                "departure_time": "2022-10-23 16:15:00",
                "arrival_location": "Manchester",
                "arrival_time": "2022-10-23 17:05:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "2022-10-23 18:25:00",
                "arrival_location": "Bristol",
                "arrival_time": "2022-10-23 19:30:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "2022-10-23 06:20:00",
                "arrival_location": "Manchester",
                "arrival_time": "2022-10-23 07:20:00"
            },
            {
                "departure_location": "Portsmouth",
                "departure_time": "2022-10-23 12:00:00",
                "arrival_location": "Dundee",
                "arrival_time": "2022-10-23 14:00:00"
            },
            {
                "departure_location": "Dundee",
                "departure_time": "2022-10-23 10:00:00",
                "arrival_location": "Portsmouth",
                "arrival_time": "2022-10-23 12:00:00"
            },
            {
                "departure_location": "Edinburgh",
                "departure_time": "2022-10-23 18:30:00",
                "arrival_location": "Cardiff",
                "arrival_time": "2022-10-23 20:00:00"
            },
            {
                "departure_location": "Southampton",
                "departure_time": "2022-10-23 12:00:00",
                "arrival_location": "Manchester",
                "arrival_time": "2022-10-23 13:30:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "2022-10-23 19:00:00",
                "arrival_location": "Southampton",
                "arrival_time": "2022-10-23 20:30:00"
            },
            {
                "departure_location": "Birmingham",
                "departure_time": "2022-10-23 16:00:00",
                "arrival_location": "Newcastle",
                "arrival_time": "2022-10-23 17:30:00"
            },
            {
                "departure_location": "Newcastle",
                "departure_time": "2022-10-23 06:00:00",
                "arrival_location": "Birmingham",
                "arrival_time": "2022-10-23 07:30:00"
            },
            {
                "departure_location": "Aberdeen",
                "departure_time": "2022-10-23 07:00:00",
                "arrival_location": "Portsmouth",
                "arrival_time": "2022-10-23 09:00:00"
            }
        ]

        travel_details_objects = []

        for travel_detail in travel_details:
            for travel_type_id in range(1,4):
                if travel_type_id in [2,3] and travel["arrival_location"] in ["Aberdeen", "Dundee"]:
                    continue
                travel = travel_detail.copy()
                travel["travel_type_id"] = travel_type_id
                travel["departure_location_id"] = locations[travel["departure_location"]]
                travel["arrival_location_id"] = locations[travel["arrival_location"]]

                if travel_type_id in [2,3]:
                    total_time = datetime.strptime(travel["arrival_time"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(travel["departure_time"], "%Y-%m-%d %H:%M:%S")
                    if travel_type_id == 2:
                        total_time *= 4
                    elif travel_type_id == 3:
                        total_time *= 9
                    travel["arrival_time"] = (datetime.strptime(travel["departure_time"], "%Y-%m-%d %H:%M:%S") + total_time).strftime("%Y-%m-%d %H:%M:%S")

                travel_details_objects.append(travel)

        for travel in travel_details_objects:
            travel["departure_time"] = datetime.strptime(travel["departure_time"], "%Y-%m-%d %H:%M:%S")
            travel["arrival_time"] = datetime.strptime(travel["arrival_time"], "%Y-%m-%d %H:%M:%S")
            del travel["departure_location"]
            del travel["arrival_location"]

        travel_details_objects = [TravelDetailTable(**travel) for travel in travel_details_objects]

        session.add_all(travel_details_objects)
        session.commit()

    except Exception as err:
        print(err)
