"""
    Generate Report Module

    Description:
    - This module is responsible for generating report.

"""

# Importing Python packages
from io import BytesIO
from datetime import (datetime)
from reportlab.lib.pagesizes import (letter, landscape)
from reportlab.lib.styles import (getSampleStyleSheet)
from reportlab.lib.units import (inch)
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)

# Importing Flask packages

# Importing from project files
# from .configuration import (TABLE_STYLE)


TABLE_STYLE = [
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0, 0), (-1, -1), "#333333"),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BACKGROUND", (0, 0), (-1, 0), "#d3d3d3"),
    ("BACKGROUND", (0, 1), (-1, -1), "#f3f3f3"),
    ("GRID", (0, 0), (-1, -1), 1, "#999999"),
]

# --------------------------------------------------------------------------------------------------


user_details = {
    "name": "John Doe",
    "email": "johndoe@email.com",
    "username": "johndoe"
}

booking_details = {
    "flight": "ABC123",
    "hotel": "Hilton",
    "car_rental": "Enterprise",
    "activities": "City tour"
}


def generatereport(
    user_details: dict, booking_details: dict,
):
    """
        Generate Report

        Description:
        - This function is responsible for generating report.

        Parameters:
        - **user_details** (list): User details.
        - **booking_details** (list): Booking details.

        Returns:
        - **generated_report** (bytes): Generated report.

    """

    # Set up the PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(
        letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Add the header with the current datetime
    header = [
        [
            Paragraph("<b>Travel Booking App</b>", styles["Heading1"]),
            "",
            Paragraph(datetime.now().strftime(
                "%Y-%m-%d %H:%M"), styles["Normal"]),
        ]
    ]
    header_table = Table(header, colWidths=[6*inch, 3*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TEXTCOLOR", (0, 0), (-1, -1), styles["Heading1"].textColor),
        ("BACKGROUND", (0, 0), (-1, 0), "#d3d3d3"),
    ]))

    # Add the user details
    user_table_data = [["User Details", ""]]
    for detail in user_details:
        user_table_data.append([f"{detail}:", user_details[detail]])
    user_table = Table(user_table_data, colWidths=[3.5*inch, 4.5*inch])
    user_table.setStyle(TableStyle(TABLE_STYLE))

    # Add the booking details
    booking_table_data = [["Booking Details", ""]]
    for detail in booking_details:
        booking_table_data.append([f"{detail}:", booking_details[detail]])
    booking_table = Table(booking_table_data, colWidths=[3.5*inch, 4.5*inch])
    booking_table.setStyle(TableStyle(TABLE_STYLE))

    # Add the user and booking tables to the PDF document
    doc.build([header_table, Spacer(0, 0.25*inch),
              user_table, Spacer(0, 0.5*inch), booking_table])

    return buffer


if __name__ == "__main__":
    # Generate the report
    buffer = generatereport(user_details, booking_details)

    # Save the PDF to a file
    with open("travel_booking.pdf", "wb") as f:
        f.write(buffer.getvalue())
