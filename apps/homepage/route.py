"""
    Homepage Module

    Description:
    - This module is responsible for getting homepage data.

"""

# Importing Python packages
from sqlalchemy import (select)
from sqlalchemy.orm import (Session)

# Importing Flask packages
from flask import (Blueprint, render_template, request)

# Importing from project files
from database.session import (get_session)
from apps.location.model import (LocationTable)
from apps.travel_type.model import (TravelTypeTable)
from apps.user.model import (UserTable)

homepage_router = Blueprint(
    name="HomePage",
    import_name=__name__,
    url_prefix="/",
)


# --------------------------------------------------------------------------------------------------


# Get homepage route
@homepage_router.route("/", methods=["GET", "POST"])
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

        query = select(UserTable).where(UserTable.is_deleted == False,
                                        UserTable.username != "admin")
        users = db_session.execute(query).scalars().all()

        return render_template("index.html",
                departure_locations=response["departure_locations"],
                arrival_locations=response["arrival_locations"],
                travel_types=response["travel_types"],
                users=users,
                response={},
                homepage=True
            )

    except Exception as err:
        db_session.rollback()
        return ({"success": False, "message": "Something went wrong", "data": response},
                500, {"ContentType": "application/json"})
