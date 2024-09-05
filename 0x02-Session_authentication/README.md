# Session Authentication

This project implements a Session Authentication system for a simple HTTP API. It builds upon the Basic Authentication system and introduces concepts such as session management, cookies, and user sessions.

## Files

- `api/v1/app.py`: Main application file
- `api/v1/views/index.py`: Basic endpoints of the API
- `api/v1/views/users.py`: User-related endpoints
- `api/v1/views/session_auth.py`: Session authentication endpoints
- `api/v1/auth/auth.py`: Base authentication class
- `api/v1/auth/basic_auth.py`: Basic authentication class
- `api/v1/auth/session_auth.py`: Session authentication class
- `api/v1/auth/session_exp_auth.py`: Session authentication with expiration
- `api/v1/auth/session_db_auth.py`: Session authentication with database storage
- `models/base.py`: Base model
- `models/user.py`: User model
- `models/user_session.py`: UserSession model for database storage

## Setup

1. Install dependencies:

pip3 install -r requirements.txt

2. Set environment variables:

export API_HOST=0.0.0.0
export API_PORT=5000
export AUTH_TYPE=session_auth
export SESSION_NAME=_my_session_id
export SESSION_DURATION=60

3. Run the application:

python3 -m api.v1.app

## Authentication Types

- `auth`: Base authentication
- `basic_auth`: Basic authentication
- `session_auth`: Session authentication
- `session_exp_auth`: Session authentication with expiration
- `session_db_auth`: Session authentication with database storage

To switch between authentication types, change the `AUTH_TYPE` environment variable.

## Testing

Use curl commands to test the API endpoints. Examples are provided in each task description.

## Requirements

- Python 3.7
- Flask
- Flask-CORS
- Requests
