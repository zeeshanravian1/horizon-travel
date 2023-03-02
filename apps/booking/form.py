"""
    Authentication Forms

    Description:
    - This module is responsible for authentication forms.
"""

# Importing Python packages

# Importing Flask packages
from flask_wtf import (FlaskForm)
from wtforms import (BooleanField, PasswordField, StringField, SubmitField, DateTimeField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length)

# Importing from project files


# --------------------------------------------------------------------------------------------------

class UpdateBookingForm(FlaskForm):
    """
        Booking Form
        
        Description:
        - This class is responsible for booking form.
        
        Parameters:
        - travel_type: Travel type.
        - departure_location: Departure location.
        - arrival_location: Arrival location.
        - departure_time: Departure time.
        - arrival_time: Arrival time.

        Returns:
        - Booking form.

    """
    
    travel_type = StringField('Travel Type', validators=[Length(min=1, max=2_55)])
    departure_location = StringField('Departure Location', validators=[Length(min=1, max=2_55)])
    arrival_location = StringField('Arrival Location', validators=[Length(min=1, max=2_55)])
    departure_time = DateTimeField('Departure Time')
    arrival_time = DateTimeField('Arrival Time')
    submit = SubmitField('Update Booking')