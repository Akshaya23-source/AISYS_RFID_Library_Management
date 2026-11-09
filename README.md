RFID-Based Library Management System

Project Overview

This project is a web-based RFID Library Management System developed using Python Flask and SQLite.

It demonstrates book management, member management, RFID tag lookup, book issue and return operations, and a dashboard.

Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

Features

- Book registration and listing
- Member registration and listing
- RFID tag association and lookup using a mock RFID service
- Book issue and return management
- Dashboard with library statistics

Project Structure

AISYS_RFID_Library/
├── app/
│   ├── routes.py
│   ├── db.py
│   ├── services/
│   ├── templates/
│   └── static/
├── documentation/
├── requirements.txt
└── run.py

Installation

1. Install Python.

2. Install dependencies:
   
   "pip install -r requirements.txt"

3. Run the application using the project's configured entry point.

4. Open the local Flask URL displayed in the terminal.

RFID Integration

The current prototype uses a mock RFID service. Physical RFID hardware integration is not included.

Current Limitations

- Real RFID reader integration is pending.
- NCIP/SIP2 integration is pending.
- Advanced authentication and role-based access control are pending.
- Spreadsheet migration and automated testing are pending.

Documentation

Refer to the "documentation" folder for the technical implementation guide and presentation.
