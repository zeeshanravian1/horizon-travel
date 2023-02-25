"""
    Homepage Module

    Description:
    - This module is responsible for getting homepage date.

"""

# Importing Python packages
from sqlalchemy import (select)
from sqlalchemy.orm import (Session)

# Importing Flask packages
from flask import (Blueprint)

# Importing from project files
from database.session import (get_session)
from apps.location.model import (LocationTable)
from apps.travel_type.model import (TravelTypeTable)

homepage_router = Blueprint(
    name="HomePage",
    import_name=__name__,
    url_prefix="/homepage",
)


# --------------------------------------------------------------------------------------------------


# Create a single location
@homepage_router.get("/")
def get_homepage(
    db_session: Session = get_session()
):
    """
        Get data for homepage

        Description:
        - This method is used to geta data for homepage

        Parameters:
        - **None**

        Returns:
        Homepage details along with following information:
        - **departure_locations** (LIST): List of departure locations.
        - **arrival_locations** (LIST): List of arrival locations.
        - **travel_types** (LIST): List of travel types.

    """
    print("Calling get_homepage method")

    response = {}

    try:
        query = select(LocationTable).where(LocationTable.is_deleted == False)
        result = db_session.execute(query).scalars().all()

        if result:
            locations = [location.name for location in result]

            response["departure_locations"] = locations
            response["arrival_locations"] = locations

        query = select(TravelTypeTable).where(TravelTypeTable.is_deleted == False)
        result = db_session.execute(query).scalars().all()

        if result:
            travel_types = [travel_type.name for travel_type in result]

            response["travel_types"] = travel_types

        return ({"success": True, "message": "Data fetched successfully", "data": response},
                200, {"ContentType": "application/json"})

    except Exception as err:
        print("error", err)
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": response},
                500, {"ContentType": "application/json"})
