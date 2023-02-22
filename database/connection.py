"""
    Database Module

    Description:
    - This module is used to configure database connection.

"""

# Importing Python packages
from sqlalchemy import (MetaData)
from sqlalchemy import (Engine, create_engine)
from sqlalchemy.orm import (DeclarativeBase, declarative_base)

# Importing Flask packages

# Importing from project files
from .configuration import (DATABASE_URL)


# --------------------------------------------------------------------------------------------------


engine: Engine = create_engine(url=DATABASE_URL)
metadata: MetaData = MetaData()
Base: DeclarativeBase = declarative_base(metadata=metadata)
