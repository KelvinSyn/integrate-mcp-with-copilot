# Mergington High School Activities API

A FastAPI application that allows students to view, sign up for, and unregister from extracurricular activities at Mergington High School.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Data Model](#data-model)
- [Error Handling](#error-handling)

## Features

- 🔍 View all available extracurricular activities
- ✍️ Sign up for activities
- 🗑️ Unregister from activities
- 📊 Track participant counts and availability
- 🔒 Validate signup capacity limits
- 📖 Interactive API documentation with OpenAPI (Swagger UI)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or install directly:

   ```bash
   pip install fastapi uvicorn
   ```

2. **Run the application**:

   Navigate to the src directory and start the server:

   ```bash
   cd src
   uvicorn app:app --reload
   ```

   The `--reload` flag enables auto-reloading during development.

3. **Access the application**:
   - **Web Interface**: http://localhost:8000
   - **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
   - **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Documentation

This API uses **OpenAPI 3.0** specification and provides interactive documentation through:

### Swagger UI (`/docs`)

An interactive interface where you can:
- View all available endpoints
- See request/response schemas
- Test API calls directly in the browser
- View example requests and responses

### ReDoc (`/redoc`)

A clean, readable documentation interface with:
- Detailed endpoint descriptions
- Request/response examples
- Schema definitions
- Easy navigation

Both documentation interfaces are automatically generated from the API code and are always up-to-date.

## API Endpoints

| Method | Endpoint                                      | Description                                                         |
| ------ | --------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/`                                           | Redirects to the web interface                                      |
| GET    | `/activities`                                 | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup`          | Sign up a student for an activity                                   |
| DELETE | `/activities/{activity_name}/unregister`      | Unregister a student from an activity                               |

### Endpoint Details

#### GET `/activities`

Returns a list of all available activities with complete details.

**Response Example**:
```json
{
  "Chess Club": {
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
  },
  "Programming Class": {
    "description": "Learn programming fundamentals and build software projects",
    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
    "max_participants": 20,
    "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
  }
}
```

#### POST `/activities/{activity_name}/signup`

Sign up a student for an activity.

**Parameters**:
- `activity_name` (path): Name of the activity (e.g., "Chess Club")
- `email` (query): Student's email address (e.g., "student@mergington.edu")

**Example Request**:
```bash
POST /activities/Chess Club/signup?email=newstudent@mergington.edu
```

**Success Response** (200):
```json
{
  "message": "Signed up newstudent@mergington.edu for Chess Club"
}
```

**Error Responses**:
- `404`: Activity not found
- `400`: Student is already signed up

#### DELETE `/activities/{activity_name}/unregister`

Unregister a student from an activity.

**Parameters**:
- `activity_name` (path): Name of the activity
- `email` (query): Student's email address

**Example Request**:
```bash
DELETE /activities/Chess Club/unregister?email=student@mergington.edu
```

**Success Response** (200):
```json
{
  "message": "Unregistered student@mergington.edu from Chess Club"
}
```

**Error Responses**:
- `404`: Activity not found
- `400`: Student is not signed up for this activity

## Usage Examples

### Using cURL

**Get all activities**:
```bash
curl http://localhost:8000/activities
```

**Sign up for an activity**:
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
```

**Unregister from an activity**:
```bash
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/unregister?email=newstudent@mergington.edu"
```

### Using Python Requests

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Get all activities
response = requests.get(f"{base_url}/activities")
activities = response.json()
print(activities)

# Sign up for an activity
response = requests.post(
    f"{base_url}/activities/Chess Club/signup",
    params={"email": "student@mergington.edu"}
)
print(response.json())

# Unregister from an activity
response = requests.delete(
    f"{base_url}/activities/Chess Club/unregister",
    params={"email": "student@mergington.edu"}
)
print(response.json())
```

### Using JavaScript (Fetch API)

```javascript
// Base URL
const baseUrl = "http://localhost:8000";

// Get all activities
fetch(`${baseUrl}/activities`)
  .then(response => response.json())
  .then(data => console.log(data));

// Sign up for an activity
fetch(`${baseUrl}/activities/Chess Club/signup?email=student@mergington.edu`, {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));

// Unregister from an activity
fetch(`${baseUrl}/activities/Chess Club/unregister?email=student@mergington.edu`, {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Data Model

The application uses a simple, in-memory data model:

### Activities

Each activity is identified by its name and contains:

- **description** (string): Brief description of the activity
- **schedule** (string): When the activity takes place
- **max_participants** (integer): Maximum number of students allowed
- **participants** (array): List of student email addresses currently signed up

**Example**:
```json
{
  "Chess Club": {
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
  }
}
```

### Available Activities

The system comes pre-loaded with the following activities:
- Chess Club
- Programming Class
- Gym Class
- Soccer Team
- Basketball Team
- Art Club
- Drama Club
- Math Club
- Debate Team

### Data Persistence

⚠️ **Important**: All data is stored in memory. When the server restarts, all changes (new signups, unregistrations) will be lost and reset to the initial state.

## Error Handling

The API uses standard HTTP status codes and returns JSON error messages:

### Status Codes

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request (e.g., already signed up, not signed up)
- `404 Not Found`: Resource not found (e.g., activity doesn't exist)
- `422 Unprocessable Entity`: Validation error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**Activity not found**:
```json
{
  "detail": "Activity not found"
}
```

**Student already signed up**:
```json
{
  "detail": "Student is already signed up"
}
```

**Student not signed up**:
```json
{
  "detail": "Student is not signed up for this activity"
}
```

## Development

### Running in Development Mode

Use the `--reload` flag to enable auto-reloading when code changes:

```bash
uvicorn app:app --reload
```

### Running on a Different Port

```bash
uvicorn app:app --port 8080
```

### Running on a Different Host

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Contributing

Interested in contributing? Check out the [Contributing Guidelines](../CONTRIBUTING.md) to get started!

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
