"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Pydantic models for request validation
class ActivityCreate(BaseModel):
    description: str
    schedule: str
    max_participants: int

class ActivityUpdate(BaseModel):
    description: Optional[str] = None
    schedule: Optional[str] = None
    max_participants: Optional[int] = None

class AttendanceRecord(BaseModel):
    email: str
    attended: bool
    date: str

# In-memory activity database
activities = {
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
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"]
    }
}

# In-memory notifications database
# WARNING: Data will be lost on application restart. Use a database for production.
notifications = []

# In-memory attendance tracking
# WARNING: Data will be lost on application restart. Use a database for production.
attendance_records = {}

# Simple user roles
# NOTE: This is a simplified demo implementation. In production, use proper
# authentication (OAuth, JWT tokens, etc.) instead of trusting client headers.
user_roles = {
    "admin@mergington.edu": "admin",
    "teacher@mergington.edu": "teacher",
    "michael@mergington.edu": "student",
    "daniel@mergington.edu": "student",
    "emma@mergington.edu": "student",
    "sophia@mergington.edu": "student"
}

def create_notification(message: str, target_users: List[str] = None):
    """Helper function to create notifications"""
    notification = {
        "id": len(notifications),
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "target_users": target_users or []  # Empty list means all users
    }
    notifications.append(notification)
    return notification

def is_admin_or_teacher(email: Optional[str]) -> bool:
    """Check if user has admin or teacher role"""
    if not email:
        return False
    role = user_roles.get(email, "student")
    return role in ["admin", "teacher"]


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    
    # Create notification
    create_notification(
        f"{email} signed up for {activity_name}",
        [email]
    )
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    
    # Create notification
    create_notification(
        f"{email} unregistered from {activity_name}",
        [email]
    )
    
    return {"message": f"Unregistered {email} from {activity_name}"}


# Notification endpoints
@app.get("/notifications")
def get_notifications(user_email: Optional[str] = None):
    """Get notifications for a user or all notifications"""
    if user_email:
        # Return notifications for specific user
        user_notifications = [
            n for n in notifications
            if not n["target_users"] or user_email in n["target_users"]
        ]
        return user_notifications
    return notifications


# Admin/Teacher endpoints for activity management
@app.post("/admin/activities")
def create_activity(
    activity_name: str,
    activity: ActivityCreate,
    user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    """Create a new activity (admin/teacher only)"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    if activity_name in activities:
        raise HTTPException(status_code=400, detail="Activity already exists")
    
    activities[activity_name] = {
        "description": activity.description,
        "schedule": activity.schedule,
        "max_participants": activity.max_participants,
        "participants": []
    }
    
    # Create notification for all users
    create_notification(f"New activity created: {activity_name}")
    
    return {"message": f"Activity '{activity_name}' created successfully"}


@app.put("/admin/activities/{activity_name}")
def update_activity(
    activity_name: str,
    activity: ActivityUpdate,
    user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    """Update an existing activity (admin/teacher only)"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Update only provided fields
    if activity.description is not None:
        activities[activity_name]["description"] = activity.description
    if activity.schedule is not None:
        activities[activity_name]["schedule"] = activity.schedule
    if activity.max_participants is not None:
        activities[activity_name]["max_participants"] = activity.max_participants
    
    # Notify participants
    participants = activities[activity_name]["participants"]
    create_notification(
        f"Activity '{activity_name}' has been updated",
        participants
    )
    
    return {"message": f"Activity '{activity_name}' updated successfully"}


@app.delete("/admin/activities/{activity_name}")
def delete_activity(
    activity_name: str,
    user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    """Delete an activity (admin/teacher only)"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Notify participants before deletion
    participants = activities[activity_name]["participants"]
    create_notification(
        f"Activity '{activity_name}' has been cancelled",
        participants
    )
    
    del activities[activity_name]
    
    return {"message": f"Activity '{activity_name}' deleted successfully"}


# Attendance tracking endpoints
@app.post("/admin/activities/{activity_name}/attendance")
def mark_attendance(
    activity_name: str,
    attendance: AttendanceRecord,
    user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    """Mark attendance for a student in an activity (admin/teacher only)"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Initialize attendance record for activity if not exists
    if activity_name not in attendance_records:
        attendance_records[activity_name] = []
    
    # Add attendance record
    attendance_records[activity_name].append({
        "email": attendance.email,
        "attended": attendance.attended,
        "date": attendance.date,
        "marked_by": user_email,
        "marked_at": datetime.now().isoformat()
    })
    
    return {"message": f"Attendance marked for {attendance.email}"}


@app.get("/admin/activities/{activity_name}/attendance")
def get_attendance(
    activity_name: str,
    user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    """Get attendance records for an activity (admin/teacher only)"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return attendance_records.get(activity_name, [])


# Reporting endpoints
@app.get("/admin/reports/activities")
def get_activities_report(user_email: Optional[str] = Header(None, alias="X-User-Email")):
    """Generate a report of all activities with participation statistics"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    report = []
    for name, details in activities.items():
        participant_count = len(details["participants"])
        attendance_count = len(attendance_records.get(name, []))
        
        report.append({
            "activity_name": name,
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "current_participants": participant_count,
            "available_spots": details["max_participants"] - participant_count,
            "attendance_records": attendance_count,
            "participants": details["participants"]
        })
    
    return {
        "generated_at": datetime.now().isoformat(),
        "total_activities": len(activities),
        "activities": report
    }


@app.get("/admin/reports/attendance/{activity_name}")
def get_attendance_report(
    activity_name: str,
    user_email: Optional[str] = Header(None, alias="X-User-Email")
):
    """Generate attendance report for a specific activity"""
    if not is_admin_or_teacher(user_email):
        raise HTTPException(status_code=403, detail="Admin or teacher access required")
    
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    records = attendance_records.get(activity_name, [])
    
    # Calculate attendance statistics
    total_records = len(records)
    attended_count = sum(1 for r in records if r["attended"])
    
    return {
        "activity_name": activity_name,
        "generated_at": datetime.now().isoformat(),
        "total_records": total_records,
        "attended_count": attended_count,
        "absence_count": total_records - attended_count,
        "attendance_rate": (attended_count / total_records * 100) if total_records > 0 else 0,
        "records": records
    }
