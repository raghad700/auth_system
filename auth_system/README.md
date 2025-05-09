Django Authentication API
This project is a Django-based REST API for user authentication and profile management. It provides endpoints for user registration, login, and profile retrieval, utilizing a custom user model with bcrypt password hashing and JSON Web Tokens (JWT) for secure authentication.
Features

Custom User Model: Extends Django's AbstractUser with unique email and bcrypt-based password hashing.
User Registration: Allows users to sign up with username, email, password, and optional first/last names.
User Login: Authenticates users via email and password, returning JWT access and refresh tokens.
Profile Access: Protected endpoint for authenticated users to retrieve their profile information.
JWT Authentication: Uses rest_framework_simplejwt for secure, token-based authentication.
Serializer Validation: Ensures data integrity during user creation and serialization.

Prerequisites

Python 3.8+
Django 4.2+
Django REST Framework
PyJWT
bcrypt
A database (e.g., SQLite for development, PostgreSQL for production)

Installation

Clone the Repository:
git clone <repository-url>
cd <repository-directory>


Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install django djangorestframework django-rest-framework-simplejwt bcrypt


Apply Migrations:
python manage.py makemigrations
python manage.py migrate


Create a Superuser (Optional):
python manage.py createsuperuser


Run the Development Server:
python manage.py runserver



Configuration

Settings: Ensure the following are added to your settings.py:
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',  # Your app name
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


Database: Configure your database in settings.py (default is SQLite).

JWT Settings: Customize token lifetimes in settings.py if needed:
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}



Usage
Endpoints

Register:

URL: /api/register/
Method: POST
Payload:{
    "username": "example_user",
    "email": "user@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}


Response (201 Created):{
    "user": {
        "id": 1,
        "username": "example_user",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}




Login:

URL: /api/login/
Method: POST
Payload:{
    "email": "user@example.com",
    "password": "securepassword123"
}


Response (200 OK):{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}




Profile:

URL: /api/profile/
Method: GET
Headers: Authorization: Bearer <access_token>
Response (200 OK):{
    "id": 1,
    "username": "example_user",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
}





