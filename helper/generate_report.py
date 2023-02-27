"""
    Generate Report Module

    Description:
    - This module is responsible for generating report.

"""

import datetime
from io import BytesIO
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Sample data for user and booking details
user_details = [
    ["Name", "John Doe"],
    ["Email", "john.doe@example.com"],
    ["Username", "johndoe"],
]
booking_details = [
    ["Flight", "ABC123"],
    ["Hotel", "Hilton"],
    ["Car rental", "Enterprise"],
    ["Activities", "City tour"],
]

# Set up the PDF document
buffer = BytesIO()
doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
styles = getSampleStyleSheet()
centered_style = ParagraphStyle(
    name="centered", parent=styles["Heading1"], alignment=TA_CENTER
)

# Add the header with the current datetime
header = [
    [
        Paragraph("<b>Travel Booking App</b>", styles["Heading1"]),
        "",
        Paragraph(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), styles["Normal"]),
    ]
]
header_table = Table(header, colWidths=[6*inch, 3*inch, 2*inch])
header_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TEXTCOLOR", (0,0), (-1,-1), styles["Heading1"].textColor),
    ("BACKGROUND", (0,0), (-1,0), "#d3d3d3"),
]))

# Add the user details
user_table_data = [["User Details",""]]
for detail in user_details:
    user_table_data.append([f"{detail[0]}:", detail[1]])
user_table = Table(user_table_data, colWidths=[3.5*inch, 4.5*inch])
user_table.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0,0), (-1,-1), "#333333"),
    ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BACKGROUND", (0,0), (-1,0), "#d3d3d3"),
    ("BACKGROUND", (0,1), (-1,-1), "#f3f3f3"),
    ("GRID", (0,0), (-1,-1), 1, "#999999"),
]))

# Add some space
spacer = Spacer(1, 0.25*inch)

# Add the booking details
booking_table_data = [["Booking Details",""]]
for detail in booking_details:
    booking_table_data.append([f"{detail[0]}", f"{detail[1]}"])
booking_table = Table(booking_table_data, colWidths=[3.5*inch, 4.5*inch])
booking_table.setStyle(TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0,0), (-1,-1), "#333333"),
    ("ALIGN", (0,0), (-1,-1), "LEFT"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BACKGROUND", (0,0), (-1,0), "#d3d3d3"),
    ("BACKGROUND", (0,1), (-1,-1), "#f3f3f3"),
    ("GRID", (0,0), (-1,-1), 1, "#999999"),
]))

# Add the user and booking tables to the PDF document
doc.build([header_table, Spacer(0, 0.25*inch), user_table, Spacer(0, 0.5*inch), booking_table])

# Save the PDF to a file
with open("travel_booking.pdf", "wb") as f:
    f.write(buffer.getvalue())
