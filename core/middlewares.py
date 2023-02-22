"""
    Middlewares Module

    Description:
    - This module contains all middlewares used in project.

"""

# Importing Python packages

# Importing Flask packages
from flask import (Request, Response)

# Importing from project files


# --------------------------------------------------------------------------------------------------


class CustomMiddleware:
    """
        Custom Middleware

        Description:
        - This class is used to create custom middleware.

        Parameters:
        - **app** (Flask): Flask application object. *--Required*

        Returns:
        - **response** (Response): Response object.

    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

    def process_request(self, request: Request):
        """
            Process Request

            Description:
            - This function is used to process request.

            Parameters:
            - **request** (Request): Request object. *--Required*

            Returns:
            - **None**

        """
        # Code to execute before each request
        print('CustomMiddleware: Processing request...')
        print(f'CustomMiddleware: Request path: {request.path}')

    def process_response(self, request: Request, response: Response):
        """
            Process Response

            Description:
            - This function is used to process response.

            Parameters:
            - **request** (Request): Request object. *--Required*
            - **response** (Response): Response object. *--Required*

            Returns:
            - **response** (Response): Response object.

        """
        # Code to execute after each request
        print('CustomMiddleware: Processing response...')
        print(f'CustomMiddleware: Request path: {request.path}')
        print(f'CustomMiddleware: Response status code: {response.status_code}')
        return response
