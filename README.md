# Student Registration System

## Overview
A Flask-based web application for managing student registrations with an admin dashboard. The system allows students to register with their details and photos, while administrators can view, edit, and manage all registered students.

## Recent Changes
- **October 18, 2025**: Enhanced registration form features
  - **Dynamic LGA Dropdown**: LGAs now populate immediately when a state is selected (both registration and edit forms)
  - **School "Other" Option**: Added "Other" option to school dropdown with custom text input field
  - **Multi-Unit Selection**: Changed unit field to multi-select with maximum 3 units allowed
  - Units are stored as comma-separated values in database
  - Added client-side validation for unit selection limit
  - Fixed form validation to support custom school names

- **October 18, 2025**: Initial setup for Replit environment
  - Installed Python 3.11 and all dependencies
  - Configured gunicorn server on port 5000
  - Updated .gitignore for Python/Flask project
  - Set up workflow for production deployment
  - Website is fully responsive (mobile, tablet, desktop)

## Project Structure
```
├── app.py                 # Main Flask application
├── models.py              # Database models (Student, Admin)
├── forms.py               # WTForms for registration and login
├── admin.py               # Admin blueprint (dashboard, login, CRUD)
├── public.py              # Public blueprint (home, registration)
├── export_users.py        # Admin will be able  to export the database in excel format
├── templates/             # HTML templates
├── static/                # Static assets (CSS, JS, images)
├── data/                  # JSON data files (states, schools, units)
└── requirements.txt       # Python dependencies
└── users_data.xlsx        # users information

```

## Features
- **Student Registration**: Form with personal details, photo upload, school selection
- **Admin Dashboard**: Login-protected interface to view and manage students
- **Database**: SQLite database with Student and Admin models
- **File Upload**: Student photo management
- **Dynamic Forms**: State/LGA cascading dropdowns, school and unit selection

## Technology Stack
- **Backend**: Flask 3.1.2
- **Database**: SQLite for Local and Postgres for production
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Server**: Gunicorn (production)

## Default Admin Credentials
- Secure admin login (with password hashing)
- Support for multiple admins
- Total Admins

## Database Schema
- **Student**: first_name, middle_name, last_name, sex, state, lga, dob, email, phone, ppa, school, unit, room_allocated, photo_filename
- **Admin**: email, password_hash
- Secure admin login (with password hashing)
- Support for multiple admins


## Excel
- **Student**: first_name, middle_name, last_name, sex, state, lga, dob, email, phone, ppa, school, unit, room_allocated, photo_filename
- **Admin**: email, password_hash

## Running the Application
The application runs automatically via the configured workflow:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port app:app
```

## Environment
- Port: port
- FLASK_ENV=development
- heroku config:set FLASK_ENV=production
- Host: 8.0.8.0
- Database: SQLite (app.db)
- Upload Directory: static/uploads/
# publicity
# publicity
