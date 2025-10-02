# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install -r ../requirements.txt
   ```
   
   Or manually:
   
   ```
   pip install fastapi uvicorn sqlalchemy
   ```

2. Run the application:

   ```
   python -m uvicorn app:app --reload
   ```
   
   The database will be automatically created and initialized with sample data on first startup.

3. Open your browser and go to:
   - Web interface: http://localhost:8000/
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

## Data Storage

All data is stored in a **SQLite database** (`data/activities.db`) for persistence. The database is automatically created and initialized with sample data when the application starts for the first time.

### Database Tables

- **activities**: Stores activity information (name, description, schedule, max_participants)
- **participants**: Stores student signups (email, activity_id)

The data persists across server restarts. See [MIGRATION.md](../MIGRATION.md) for more details about the database structure and migration from the previous in-memory storage.
