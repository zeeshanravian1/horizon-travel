"""
    Session Module

    Description:
    - This module is used to configure database session.

"""

# Importing Python packages
from sqlalchemy.orm import (Session, sessionmaker)

# Importing Flask packages

# Importing from project files
from .connection import (engine)


# --------------------------------------------------------------------------------------------------


SessionLocal: Session = sessionmaker(autoflush=True, bind=engine, expire_on_commit=True)


def get_session():
    """
        Get session

        Description:
        - This function is used to get session.

        Parameters:
        - **None**

        Returns:
        - **session** (AsyncSession): Session.

    """
    print("Calling get_session method")

    session: Session = SessionLocal()

    try:
        return session

    except Exception as err:
        session.rollback()
        raise err

    finally:
        session.close()
