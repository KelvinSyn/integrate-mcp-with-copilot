# Database Migration Guide

## Overview

The Mergington High School Activities API has been migrated from an in-memory data storage to a persistent SQLite database using SQLAlchemy ORM.

## What Changed

### Before
- Activities and participants were stored in a Python dictionary in memory
- Data was lost when the server restarted
- No data persistence between sessions

### After
- Activities and participants are stored in a SQLite database
- Data persists across server restarts
- Database is automatically created and initialized on first run

## Database Structure

The application uses two tables:

### Activities Table
- `id`: Primary key (auto-generated)
- `name`: Activity name (unique)
- `description`: Activity description
- `schedule`: Activity schedule
- `max_participants`: Maximum number of participants

### Participants Table
- `id`: Primary key (auto-generated)
- `email`: Student email
- `activity_id`: Foreign key to activities table

## Migration Steps

### For New Installations

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application**:
   ```bash
   cd src
   python -m uvicorn app:app --reload
   ```

   The database will be automatically created at `src/data/activities.db` with sample data on first startup.

### For Existing Deployments

If you're upgrading from the in-memory version:

1. **Backup any custom data** (if you modified the in-memory activities dictionary)

2. **Update dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database** (optional, only if you want to pre-populate):
   ```bash
   cd src
   python init_db.py
   ```

4. **Start the application**:
   ```bash
   python -m uvicorn app:app --reload
   ```

## Database Management

### Location
The SQLite database is stored at: `src/data/activities.db`

### Backup
To backup the database, simply copy the database file:
```bash
cp src/data/activities.db src/data/activities.db.backup
```

### Reset Database
To reset the database to initial sample data:
```bash
cd src
rm -rf data/activities.db
python init_db.py
```

### Manual Database Inspection
You can inspect the database using sqlite3:
```bash
sqlite3 src/data/activities.db
.tables
.schema activities
SELECT * FROM activities;
SELECT * FROM participants;
.quit
```

## API Compatibility

The API endpoints remain **100% backward compatible**:
- `GET /activities` - Returns the same JSON structure as before
- `POST /activities/{activity_name}/signup?email=...` - Works exactly the same
- `DELETE /activities/{activity_name}/unregister?email=...` - Works exactly the same

No changes are required to client applications or the web frontend.

## Technical Details

### Technologies Used
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight, file-based database (no server required)
- **FastAPI Depends**: Dependency injection for database sessions

### Files Added
- `src/database.py`: Database configuration and session management
- `src/models.py`: SQLAlchemy ORM models
- `src/init_db.py`: Database initialization script
- `MIGRATION.md`: This migration guide

### Files Modified
- `src/app.py`: Updated to use database instead of in-memory dictionary
- `requirements.txt`: Added SQLAlchemy dependency
- `.gitignore`: Added database files to ignore list

## Troubleshooting

### Issue: Database not found
**Solution**: The database is created automatically on first run. Make sure the `src/data/` directory can be created.

### Issue: Permission denied creating database
**Solution**: Ensure the application has write permissions to the `src/` directory.

### Issue: Data not persisting
**Solution**: Check that:
1. The database file exists at `src/data/activities.db`
2. The file has write permissions
3. You're not running multiple instances pointing to different directories

## Migration to PostgreSQL (Future)

If you need to migrate to PostgreSQL for production:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `src/database.py`:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
   ```

3. The same models and application code will work without modification.
