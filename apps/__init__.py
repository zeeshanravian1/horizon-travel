"""
    Apps Module

    Description:
    - This module contains apps routers.

"""

from .auth import (auth_router)
from .booking import (booking_router)
from .expense import (expense_router)
from .location import (location_router)
from .max_seat import (max_seat_router)
from .price_category import (price_category_router)
from .travel_detail import (travel_detail_router)
from .travel_type import (travel_type_router)
from .user import (user_router)
from .homepage import (homepage_router)
from .records import (records_router)
