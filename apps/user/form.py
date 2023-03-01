"""
    Authentication Forms

    Description:
    - This module is responsible for authentication forms.
"""

# Importing Python packages

# Importing Flask packages
from flask_wtf import (FlaskForm)
from wtforms import (BooleanField, PasswordField, StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length)

# Importing from project files


# --------------------------------------------------------------------------------------------------

class UpdateProfileForm(FlaskForm):
    """
        Registration Form
        
        Description:
        - This class is responsible for registration form.
        
        Parameters:
        - name: User's name.
        - contact: User's contact.
        - username: User's username.
        - email: User's email.
        - password: User's password.
        - conform_password: User's conform password.

        Returns:
        - Registration form.

    """
    name = StringField('Name', validators=[Length(min=1, max=2_55)])
    contact = StringField('Contact', validators=[Length(min=1, max=2_55)])
    username = StringField('Username', validators=[Length(min=1, max=2_55)])
    email = StringField('E-Mail Address', validators=[Email()])
    password = PasswordField('Password', validators=[])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update Profile')


