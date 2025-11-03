"""
Unit tests for the High School Management System API endpoints.

These tests verify individual endpoint functionality in isolation.
"""

import pytest
from fastapi import status


class TestRootEndpoint:
    """Tests for the root endpoint (/)"""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/index.html"


class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint"""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns 200 OK"""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary"""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_activities_contains_all_activities(self, client):
        """Test that GET /activities returns all expected activities"""
        response = client.get("/activities")
        data = response.json()
        
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Soccer Team", "Basketball Team", "Art Club",
            "Drama Club", "Math Club", "Debate Team"
        ]
        
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_get_activities_has_correct_structure(self, client):
        """Test that each activity has the correct data structure"""
        response = client.get("/activities")
        data = response.json()
        
        # Test structure of first activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_participants_are_lists(self, client):
        """Test that all activities have participants as lists"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_for_valid_activity_returns_200(self, client):
        """Test that signing up for a valid activity returns 200 OK"""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_signup_adds_student_to_activity(self, client):
        """Test that signup actually adds the student to the activity"""
        email = "newstudent@mergington.edu"
        
        # Sign up
        client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Verify student was added
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]
    
    def test_signup_returns_success_message(self, client):
        """Test that signup returns appropriate success message"""
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404"""
        response = client.post(
            "/activities/NonexistentClub/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_signup_for_nonexistent_activity_returns_error_message(self, client):
        """Test that 404 response contains appropriate error message"""
        response = client.post(
            "/activities/NonexistentClub/signup",
            params={"email": "student@mergington.edu"}
        )
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Activity not found"
    
    def test_duplicate_signup_returns_400(self, client):
        """Test that duplicate signup returns 400 Bad Request"""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_duplicate_signup_returns_error_message(self, client):
        """Test that duplicate signup returns appropriate error message"""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Student is already signed up"
    
    def test_signup_with_special_characters_in_activity_name(self, client):
        """Test signup works with URL-encoded activity names"""
        # Note: FastAPI handles URL encoding automatically
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_multiple_students_can_signup_for_same_activity(self, client):
        """Test that multiple different students can sign up for the same activity"""
        activity_name = "Chess Club"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify all students were added
        response = client.get("/activities")
        data = response.json()
        for email in emails:
            assert email in data[activity_name]["participants"]


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_from_valid_activity_returns_200(self, client):
        """Test that unregistering from a valid activity returns 200 OK"""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == status.HTTP_200_OK
    
    def test_unregister_removes_student_from_activity(self, client):
        """Test that unregister actually removes the student from the activity"""
        email = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        # Unregister
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Verify student was removed
        response = client.get("/activities")
        data = response.json()
        assert email not in data[activity_name]["participants"]
    
    def test_unregister_returns_success_message(self, client):
        """Test that unregister returns appropriate success message"""
        email = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404"""
        response = client.delete(
            "/activities/NonexistentClub/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_unregister_from_nonexistent_activity_returns_error_message(self, client):
        """Test that 404 response contains appropriate error message"""
        response = client.delete(
            "/activities/NonexistentClub/unregister",
            params={"email": "student@mergington.edu"}
        )
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Activity not found"
    
    def test_unregister_when_not_signed_up_returns_400(self, client):
        """Test that unregistering when not signed up returns 400 Bad Request"""
        email = "notsignedup@mergington.edu"
        
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_unregister_when_not_signed_up_returns_error_message(self, client):
        """Test that unregister error returns appropriate error message"""
        email = "notsignedup@mergington.edu"
        
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Student is not signed up for this activity"
    
    def test_unregister_with_special_characters_in_activity_name(self, client):
        """Test unregister works with URL-encoded activity names"""
        # First signup a new student
        email = "test@mergington.edu"
        client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Then unregister
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK


class TestEndpointParameterValidation:
    """Tests for parameter validation across endpoints"""
    
    def test_signup_requires_email_parameter(self, client):
        """Test that signup endpoint requires email parameter"""
        response = client.post("/activities/Chess Club/signup")
        # FastAPI will return 422 for missing required parameters
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_unregister_requires_email_parameter(self, client):
        """Test that unregister endpoint requires email parameter"""
        response = client.delete("/activities/Chess Club/unregister")
        # FastAPI will return 422 for missing required parameters
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
