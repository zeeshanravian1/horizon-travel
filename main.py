"""
    Main file for project

    Description:
    - This program is main file for project.
    - It is used to create Flask object and add all routes to it.

"""

from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy.orm import (Session)

from core import (CORS_ALLOW_HEADERS, CORS_ALLOW_METHODS, CORS_ALLOW_ORIGINS)
from database import (metadata)
from database.connection import (engine)
from apps.role.model import (RoleTable)
from database import (get_session)

app = Flask(__name__)
api = Api(app)


app.config["CORS_HEADERS"] = CORS_ALLOW_HEADERS
app.config["CORS_ORIGINS"] = CORS_ALLOW_ORIGINS
app.config["CORS_METHODS"] = CORS_ALLOW_METHODS


metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)


from sqlalchemy.orm import (Session, sessionmaker)

SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_session():
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
        yield session

    except Exception as err:
        session.rollback()
        raise err

    finally:
        session.close()


def insert_roles(session: Session = get_session()):
    """
        Insert roles

        Description:
        - This function is used to insert roles.

        Parameters:
        - **None**

        Returns:
        - **None**

    """
    print("Calling insert_roles method")

    # Insert admin role in database
    admin_role: RoleTable = RoleTable(role_name="admin")
    user_role: RoleTable = RoleTable(role_name="user")

    db: Session = SessionLocal()
    db.add(admin_role)
    db.add(user_role)
    db.commit()
    db.close()


insert_roles()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
# api.add_resource(TodoSimple, '/todo/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)


print("******************************************")
print(app.url_map)
print("******************************************")