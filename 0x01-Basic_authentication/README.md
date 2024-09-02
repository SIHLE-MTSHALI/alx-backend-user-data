# Basic Authentication

This project implements a Basic Authentication system for a simple HTTP API. It covers the fundamentals of authentication, Base64 encoding, and how to send the Authorization header.

## Files

- `api/v1/app.py`: Main application file
- `api/v1/views/index.py`: Basic endpoints of the API
- `api/v1/auth/auth.py`: Authentication class
- `api/v1/auth/basic_auth.py`: BasicAuth class inheriting from Auth
- `models/base.py`: Base model
- `models/user.py`: User model
- `requirements.txt`: Project dependencies

## Setup

1. Install dependencies:
pip3 install -r requirements.txt

2. Run the application:

API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app

## Routes

- `GET /api/v1/status`: Returns the status of the API
- `GET /api/v1/stats`: Returns some stats of the API
- `GET /api/v1/users`: Returns the list of users
- `GET /api/v1/users/:id`: Returns a user based on the ID
- `DELETE /api/v1/users/:id`: Deletes a user based on the ID
- `POST /api/v1/users`: Creates a new user
- `PUT /api/v1/users/:id`: Updates a user based on the ID

## Authentication

The API uses Basic Authentication. To access protected routes, include an Authorization header with a Base64 encoded string of `username:password`.
