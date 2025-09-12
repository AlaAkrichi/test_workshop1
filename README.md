# Flask Mock Login API

A simple Flask API with mock authentication using JWT tokens.

## Features

- Mock user authentication
- JWT token-based authorization
- Protected routes
- RESTful API endpoints

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### GET /
- **Description**: Home endpoint with API information
- **Authentication**: None required

### POST /login
- **Description**: Login with username and password
- **Authentication**: None required
- **Body**:
```json
{
  "username": "admin",
  "password": "password123"
}
```
- **Response**:
```json
{
  "message": "Login successful!",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "username": "admin"
}
```

### GET /protected
- **Description**: Protected route that requires authentication
- **Authentication**: Bearer token required
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
  "message": "Hello admin! This is a protected route.",
  "user": "admin",
  "timestamp": "2025-09-12T12:15:49.123456"
}
```

### GET /users
- **Description**: Get list of available mock users
- **Authentication**: None required
- **Response**:
```json
{
  "message": "Mock users for testing",
  "users": ["admin", "user1", "testuser"],
  "note": "Use these usernames with their corresponding passwords to test login"
}
```

### POST /logout
- **Description**: Mock logout endpoint
- **Authentication**: Bearer token required
- **Headers**: `Authorization: Bearer <token>`

## Mock Users

The following users are available for testing:

| Username | Password |
|----------|----------|
| admin | password123 |
| user1 | mypassword |
| testuser | test123 |

## Usage Examples

### 1. Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'
```

### 2. Access Protected Route
```bash
curl -X GET http://localhost:5000/protected \
  -H "Authorization: Bearer <your-token-here>"
```

### 3. Get Available Users
```bash
curl -X GET http://localhost:5000/users
```

## Security Notes

- This is a mock implementation for development/testing purposes
- Change the `SECRET_KEY` in production
- In a real application, use proper password hashing
- Implement token blacklisting for logout functionality
- Use HTTPS in production
