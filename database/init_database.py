"""
    Database Initialization

    Description:
    - This module is responsible for initializing database.

"""

# Importing Python packages
from random import random
from datetime import (datetime, timedelta, time)
from passlib.hash import (pbkdf2_sha256)

# Importing FastAPI packages

# Importing from project files
from apps.user.model import (UserTable)
from apps.location.model import (LocationTable)
from apps.price_category.model import (PriceCategoryTable)
from apps.travel_type.model import (TravelTypeTable)
from apps.max_seat.model import (MaxSeatTable)
from apps.travel_detail.model import (TravelDetailTable)
from apps.expense.model import (ExpenseTable)
from .configuration import (ADMIN_NAME, ADMIN_CONTACT, ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
from .session import (get_session)


# --------------------------------------------------------------------------------------------------


def update_travel_datetime(travel_detail, min_date, max_date):
    """
        Update travel datetime
        
        Description:
        - This function is used to update travel datetime.

        Parameters:
        - **travel_detail** (dict): Travel detail.
        - **min_date** (datetime): Minimum date.
        - **max_date** (datetime): Maximum date.

        Returns:
        - **travel_detail** (dict): Travel detail.
        
    """
    random_date = (min_date + (max_date - min_date) * random()).date()

    travel_detail['departure_time'] = datetime.combine(random_date, time.fromisoformat(
        travel_detail['departure_time'])).strftime("%Y-%m-%d %H:%M:%S")
    travel_detail['arrival_time'] = datetime.combine(random_date, time.fromisoformat(
        travel_detail['arrival_time'])).strftime("%Y-%m-%d %H:%M:%S")

    return travel_detail


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
        price_categories = ["business", "economy"]

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
        location_names = {location.name: location.id for location in locations}
        locations_ids = {location.id: location.name for location in locations}

        travel_details = [
            {
                "departure_location": "Newcastle",
                "departure_time": "16:45:00",
                "arrival_location": "Bristol",
                "arrival_time": "18:00:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "08:00:00",
                "arrival_location": "Newcastle",
                "arrival_time": "09:15:00"
            },
            {
                "departure_location": "Cardiff",
                "departure_time": "06:00:00",
                "arrival_location": "Edinburgh",
                "arrival_time": "07:30:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "11:30:00",
                "arrival_location": "Manchester",
                "arrival_time": "12:30:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "12:20:00",
                "arrival_location": "Bristol",
                "arrival_time": "13:20:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "07:40:00",
                "arrival_location": "London",
                "arrival_time": "08:20:00"
            },
            {
                "departure_location": "London",
                "departure_time": "11:00:00",
                "arrival_location": "Manchester",
                "arrival_time": "12:20:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "12:20:00",
                "arrival_location": "Glasgow",
                "arrival_time": "13:30:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "07:40:00",
                "arrival_location": "Glasgow",
                "arrival_time": "08:45:00"
            },
            {
                "departure_location": "Glasgow",
                "departure_time": "14:30:00",
                "arrival_location": "Newcastle",
                "arrival_time": "15:45:00"
            },
            {
                "departure_location": "Newcastle",
                "departure_time": "16:15:00",
                "arrival_location": "Manchester",
                "arrival_time": "17:05:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "18:25:00",
                "arrival_location": "Bristol",
                "arrival_time": "19:30:00"
            },
            {
                "departure_location": "Bristol",
                "departure_time": "06:20:00",
                "arrival_location": "Manchester",
                "arrival_time": "07:20:00"
            },
            {
                "departure_location": "Portsmouth",
                "departure_time": "12:00:00",
                "arrival_location": "Dundee",
                "arrival_time": "14:00:00"
            },
            {
                "departure_location": "Dundee",
                "departure_time": "10:00:00",
                "arrival_location": "Portsmouth",
                "arrival_time": "12:00:00"
            },
            {
                "departure_location": "Edinburgh",
                "departure_time": "18:30:00",
                "arrival_location": "Cardiff",
                "arrival_time": "20:00:00"
            },
            {
                "departure_location": "Southampton",
                "departure_time": "12:00:00",
                "arrival_location": "Manchester",
                "arrival_time": "13:30:00"
            },
            {
                "departure_location": "Manchester",
                "departure_time": "19:00:00",
                "arrival_location": "Southampton",
                "arrival_time": "20:30:00"
            },
            {
                "departure_location": "Birmingham",
                "departure_time": "16:00:00",
                "arrival_location": "Newcastle",
                "arrival_time": "17:30:00"
            },
            {
                "departure_location": "Newcastle",
                "departure_time": "06:00:00",
                "arrival_location": "Birmingham",
                "arrival_time": "07:30:00"
            },
            {
                "departure_location": "Aberdeen",
                "departure_time": "07:00:00",
                "arrival_location": "Portsmouth",
                "arrival_time": "09:00:00"
            }
        ]

        now = datetime.now()
        min_date = datetime(now.year, now.month, now.day)
        max_date = min_date + timedelta(days=90)

        travel_details = travel_details = [update_travel_datetime(
            travel_detail=travel_detail, min_date=min_date, max_date=max_date)
            for travel_detail in travel_details]

        travel_details_objects = []

        for travel_detail in travel_details:
            for travel_type_id in range(1, 4):
                if travel_type_id in [2, 3] and travel["arrival_location"] in ["Aberdeen", "Dundee"]:
                    continue
                travel = travel_detail.copy()
                travel["travel_type_id"] = travel_type_id
                travel["departure_location_id"] = location_names[travel["departure_location"]]
                travel["arrival_location_id"] = location_names[travel["arrival_location"]]

                if travel_type_id in [2, 3]:
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

        # Insert Expenses
        traveL_details = session.query(TravelDetailTable).all()
        travel_details = [travel.to_dict() for travel in traveL_details]

        expenses = [{"departure": "Dundee", "arrival": "Portsmouth", "expense": 100},
                    {"departure": "Portsmouth", "arrival": "Dundee", "expense": 100},
                    {"departure": "Bristol", "arrival": "Manchester", "expense": 60},
                    {"departure": "Manchester", "arrival": "Bristol", "expense": 60},
                    {"departure": "Bristol", "arrival": "Newcastle", "expense": 80},
                    {"departure": "Newcastle", "arrival": "Bristol", "expense": 80},
                    {"departure": "Bristol", "arrival": "Glasgow", "expense": 90},
                    {"departure": "Glasgow", "arrival": "Bristol", "expense": 90},
                    {"departure": "Bristol", "arrival": "London", "expense": 60},
                    {"departure": "London", "arrival": "Bristol", "expense": 60},
                    {"departure": "Manchester", "arrival": "Southampton", "expense": 70},
                    {"departure": "Southampton", "arrival": "Manchester", "expense": 70},
                    {"departure": "Cardiff", "arrival": "Edinburgh", "expense": 80},
                    {"departure": "Edinburgh", "arrival": "Cardiff", "expense": 80}]

        expenses_objects = []

        for travel_detail in travel_details:
            departure_location = locations_ids[travel_detail["departure_location_id"]]
            arrival_location = locations_ids[travel_detail["arrival_location_id"]]

            dic = {
                "travel_detail_id": travel_detail["id"],
                "price_category_id": 2,
                "cost": 75
            }

            for expense in expenses:
                if expense["departure"] == departure_location and expense["arrival"] == arrival_location:
                    if travel_detail["travel_type_id"] == 1:
                        dic["cost"] = expense["expense"]
                    elif travel_detail["travel_type_id"] == 2:
                        dic["cost"] = round(expense["expense"] * 2.5, 2)
                    elif travel_detail["travel_type_id"] == 3:
                        dic["cost"] = round(expense["expense"] / 3, 2)
                    break

            expenses_objects.append(dic)

        expenses_objects_2x = []

        for expense in expenses_objects:
            data = expense.copy()
            data["price_category_id"] = 1
            data["cost"] = round(data["cost"] * 2, 2)
            expenses_objects_2x.append(data)

        expenses_objects = expenses_objects + expenses_objects_2x

        expenses_objects = [ExpenseTable(**expense)
                            for expense in expenses_objects]

        session.add_all(expenses_objects)
        session.commit()

    except Exception as err:
        pass
