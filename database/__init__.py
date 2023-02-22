"""
    Database Module

    Description:
    - This module contains database configuration.

"""
from .base import (BaseTable)
from .configuration import (DATABASE_URL, DB_NAME)
from .connection import (metadata)
from .init_database import (insert_admin)
from .session import (get_session)
