"""
    Role APIs Module

    Description:
    - This module is responsible for handling role APIs.
    - It is used to create, get, update, delete role details.

"""

# Importing Python packages
from sqlalchemy import (delete, select, update, func)
from sqlalchemy.orm import (Session)

# Importing Flask packages
from flask_restful import (Resource, Api)
from flask import request



# Importing from project files
from database.session import (get_session)
from .exception import (ROLE_NOT_FOUND)
from .model import (RoleTable)
from .schema import (RoleCreateSchema, RoleReadSchema, RolePaginationReadSchema, RoleUpdateSchema,
                     RolePartialUpdateSchema)

# print("*********************")
# print(print(__name__))
# print("*********************")


# role_router = Blueprint(
#     name='Role',
#     import_name="role",
#     url_prefix='/role',
# )


# --------------------------------------------------------------------------------------------------


todos = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

class TodoSimple(Resource):
    def get(self, todo_id):
        return "<p>Hello, World!</p>"

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


# @role_router.route('/<role_id>/')
# def show(role_id: int):
#     try:
#         return "Role with id: " + role_id
#     except Exception as e:
#         print(e)
#         return "Error"


# # Create a single role route
# @router.post(
#     path="/",
#     status_code=status.HTTP_201_CREATED,
#     summary="Create a single role",
#     response_description="Role created successfully"
# )
# async def create_role(
#     record: RoleCreateSchema, db_session: Session = Depends(get_session)
# ) -> RoleReadSchema:
#     """
#         Create a single role.

#         Description:
#         - This method is used to create a single role.

#         Parameters:
#         Role details to be created with following fields:
#         - **role_name** (STR): Name of role. *--Required*
#             - **Allowed values:** "admin", "manager", "user"
#         - **role_description** (STR): Description of role. *--Required*

#         Returns:
#         Role details along with following information:
#         - **id** (INT): Id of role.
#         - **role_name** (STR): Name of role.
#         - **role_description** (STR): Description of role.
#         - **created_at** (DATETIME): Datetime of role creation.
#         - **updated_at** (DATETIME): Datetime of role updation.

#     """
#     print("Calling create_role method")

#     new_record = RoleTable(
#         role_name=record.role_name,
#         role_description=record.role_description
#     )

#     db_session.add(new_record)
#     await db_session.commit()
#     await db_session.refresh(new_record)

#     return RoleReadSchema.from_orm(new_record)


# # Get a single role route
# @router.get(
#     path="/{role_id}/",
#     status_code=status.HTTP_200_OK,
#     summary="Get a single role by providing id",
#     response_description="Role details fetched successfully"
# )
# async def get_role(
#     role_id: int, db_session: Session = Depends(get_session)
# ) -> RoleReadSchema:
#     """
#         Get a single role.

#         Description:
#         - This method is used to get a single role by providing id.

#         Parameters:
#         - **role_id** (INT): ID of role to be fetched. *--Required*

#         Returns:
#         Get a single role with following information:
#         - **id** (INT): Id of role.
#         - **role_name** (STR): Name of role.
#         - **role_description** (STR): Description of role.
#         - **created_at** (DATETIME): Datetime of role creation.
#         - **updated_at** (DATETIME): Datetime of role updation.

#     """
#     print("Calling get_role method")

#     query = select(RoleTable).where(RoleTable.id == role_id)
#     result = await db_session.execute(query)
#     result = result.scalars().first()

#     if not result:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"message": role_exception.ROLE_NOT_FOUND}
#         )

#     return RoleReadSchema.from_orm(result)


# # Get all roles route
# @router.get(
#     path="/",
#     status_code=status.HTTP_200_OK,
#     summary="Get all roles",
#     response_description="All roles fetched successfully"
# )
# async def get_all_roles(
#     page: int | None = 1, limit: int | None = 10,
#     db_session: Session = Depends(get_session)
# ) -> RolePaginationReadSchema:
#     """
#         Get all roles.

#         Description:
#         - This method is used to get all roles.

#         Parameters:
#         - **None**

#         Returns:
#         Get all roles with following information:
#         - **id** (INT): Id of role.
#         - **role_name** (STR): Name of role.
#         - **role_description** (STR): Description of role.
#         - **created_at** (DATETIME): Datetime of role creation.
#         - **updated_at** (DATETIME): Datetime of role updation.

#     """
#     print("Calling get_all_roles method")

#     query = select(func.count(RoleTable.id))
#     result = await db_session.execute(query)
#     total_count = result.scalar()

#     if page and limit:
#         query = select(RoleTable).where(
#             RoleTable.id > (page - 1) * limit).limit(limit)

#     result = await db_session.execute(query)
#     result = result.scalars().all()

#     return RolePaginationReadSchema(
#         total=total_count,
#         page=page,
#         limit=limit,
#         data=result
#     )


# # Update a single role route
# @router.put(
#     path="/{role_id}/",
#     status_code=status.HTTP_200_OK,
#     summary="Update a single role by providing id",
#     response_description="Role updated successfully"
# )
# async def update_role(
#     role_id: int, record: RoleUpdateSchema, db_session: Session = Depends(get_session)
# ) -> RoleReadSchema:
#     """
#         Update a single role.

#         Description:
#         - This method is used to update a single role by providing id.
#         - If any field is not provided, it will be updated with null value.

#         Parameters:
#         - **role_id** (INT): ID of role to be updated. *--Required*
#         Role details to be updated with following fields:
#         - **role_name** (STR): Name of role. *--Required*
#             - **Allowed values:** "admin", "manager", "user"
#         - **role_description** (STR): Description of role. *--Required*

#         Returns:
#         Role details along with following information:
#         - **id** (INT): Id of role.
#         - **role_name** (STR): Name of role.
#         - **role_description** (STR): Description of role.
#         - **created_at** (DATETIME): Datetime of role creation.
#         - **updated_at** (DATETIME): Datetime of role updation.

#     """
#     print("Calling update_role method")

#     query = select(RoleTable).where(RoleTable.id == role_id)
#     result = await db_session.execute(query)
#     result = result.scalars().first()

#     if not result:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"message": role_exception.ROLE_NOT_FOUND}
#         )

#     record = RoleTable(
#         role_name=record.role_name,
#         role_description=record.role_description
#     )

#     query = update(RoleTable).where(RoleTable.id == role_id).values(
#         role_name=record.role_name,
#         role_description=record.role_description
#     )
#     await db_session.execute(query)
#     await db_session.commit()




# # Partial update a single role route
# @router.patch(
#     path="/{role_id}/",
#     status_code=status.HTTP_200_OK,
#     summary="Partial update a single role by providing id",
#     response_description="Role updated successfully"
# )
# async def partial_update_role(
#     role_id: int, record: RolePartialUpdateSchema, db_session: Session = Depends(get_session)
# ) -> RoleReadSchema:
#     """
#         Partial update a single role.

#         Description:
#         - This method is used to partial update a single role by providing id.
#         - If any field is not provided, it will not be updated.

#         Parameters:
#         - **role_id**: ID of role to be updated. (INT) *--Required*
#         Role details to be updated with following fields:
#         - **role_name**: Name of role. (STR) *--Optional*
#             - **Allowed values:** "admin", "manager", "user"
#         - **role_description**: Description of role. (STR) *--Required*

#         Returns:
#         Role details along with following information:
#         - **id**: Id of role. (INT)
#         - **role_name**: Name of role. (STR)
#         - **role_description**: Description of role. (STR)
#         - **created_at**: Datetime of role creation. (DATETIME)
#         - **updated_at**: Datetime of role updation. (DATETIME)

#     """
#     print("Calling partial_update_role method")

#     query = select(RoleTable).where(RoleTable.id == role_id)
#     result = await db_session.execute(query)
#     result = result.scalars().first()

#     if not result:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"message": role_exception.ROLE_NOT_FOUND}
#         )

#     record = RoleReadSchema(**result).copy(update=record.dict(exclude_unset=True))

#     await db_session.commit()
#     await db_session.refresh(record)

#     return RoleReadSchema.from_orm(record)


# # Delete a single role route
# @router.delete(
#     path="/{role_id}/",
#     status_code=status.HTTP_200_OK,
#     summary="Delete a single role by providing id",
#     response_description="Role deleted successfully"
# )
# async def delete_role(
#     role_id: int, db_session: Session = Depends(get_session)
# ) -> JSONResponse:
#     """
#         Delete a single role.

#         Description:
#         - This method is used to delete a single role by providing id.

#         Parameters:
#         - **role_id** (INT): ID of role to be deleted. *--Required*

#         Returns:
#         - **message** (STR): Message of role deletion.

#     """
#     print("Calling delete_role method")

#     query = select(RoleTable).where(RoleTable.id == role_id)
#     result = await db_session.execute(query)
#     result = result.scalars().first()

#     if not result:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={"message": role_exception.ROLE_NOT_FOUND}
#         )

#     query = delete(RoleTable).where(RoleTable.id == role_id)
#     await db_session.execute(query)
#     await db_session.commit()

#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={"message": role_exception.ROLE_DELETED}
#     )