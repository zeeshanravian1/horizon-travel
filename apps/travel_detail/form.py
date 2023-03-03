"""
    Travel Detail Forms

    Description:
    - This module is responsible for travel detail forms.
"""

# Importing Python packages

# Importing Flask packages
from flask_wtf import (FlaskForm)
from wtforms import (StringField, SubmitField, DateTimeField, FloatField)
from wtforms.validators import (Length)

# Importing from project files


# --------------------------------------------------------------------------------------


class TravelDetailForm(FlaskForm):
    """
        Create Travel Detail Form
        
        Description:
        - This class is responsible for creating travel detail form.
        
        Parameters:
        - travel_type: Travel type.
        - departure_location: Departure location.
        - arrival_location: Arrival location.
        - departure_time: Departure time.
        - arrival_time: Arrival time.

        Returns:
        - Booking form.

    """

    departure_location = StringField('Departure Location', validators=[Length(min=1, max=2_55)])
    arrival_location = StringField('Arrival Location', validators=[Length(min=1, max=2_55)])
    departure_time = DateTimeField('Departure Time')
    arrival_time = DateTimeField('Arrival Time')
    travel_type = StringField('Travel Type', validators=[Length(min=1, max=2_55)])
    expense = FloatField('Expense')
    submit = SubmitField('Create')
