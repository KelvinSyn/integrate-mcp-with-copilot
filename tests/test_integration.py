"""
Integration tests for the High School Management System API.

These tests verify complete workflows and interactions between endpoints.
"""

import pytest
from fastapi import status


class TestStudentSignupWorkflow:
    """Integration tests for student signup workflows"""
    
    def test_complete_signup_workflow(self, client):
        """Test complete workflow: view activities, signup, verify signup"""
        # Step 1: Get activities
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        activities = response.json()
        initial_chess_participants = len(activities["Chess Club"]["participants"])
        
        # Step 2: Signup for an activity
        email = "newstudent@mergington.edu"
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Step 3: Verify signup by getting activities again
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        activities = response.json()
        assert email in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == initial_chess_participants + 1
    
    def test_signup_and_unregister_workflow(self, client):
        """Test complete workflow: signup, verify, unregister, verify"""
        email = "tempstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Step 1: Initial state
        response = client.get("/activities")
        initial_participants = response.json()[activity_name]["participants"].copy()
        
        # Step 2: Signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Step 3: Verify signup
        response = client.get("/activities")
        assert email in response.json()[activity_name]["participants"]
        
        # Step 4: Unregister
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Step 5: Verify unregister
        response = client.get("/activities")
        final_participants = response.json()[activity_name]["participants"]
        assert email not in final_participants
        assert final_participants == initial_participants


class TestMultipleActivityManagement:
    """Integration tests for managing multiple activities"""
    
    def test_student_can_join_multiple_activities(self, client):
        """Test that a student can join multiple different activities"""
        email = "multitalented@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Art Club"]
        
        for activity_name in activities_to_join:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify student is in all activities
        response = client.get("/activities")
        all_activities = response.json()
        
        for activity_name in activities_to_join:
            assert email in all_activities[activity_name]["participants"]
    
    def test_student_can_leave_one_activity_while_staying_in_others(self, client):
        """Test that leaving one activity doesn't affect other enrollments"""
        email = "selective@mergington.edu"
        activities = ["Chess Club", "Programming Class", "Math Club"]
        
        # Join all activities
        for activity_name in activities:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
        
        # Leave only Chess Club
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify still in other activities
        response = client.get("/activities")
        all_activities = response.json()
        
        assert email not in all_activities["Chess Club"]["participants"]
        assert email in all_activities["Programming Class"]["participants"]
        assert email in all_activities["Math Club"]["participants"]


class TestActivityCapacityManagement:
    """Integration tests for activity capacity scenarios"""
    
    def test_multiple_students_fill_activity(self, client):
        """Test that multiple students can fill up an activity"""
        activity_name = "Math Club"
        
        # Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])
        max_capacity = response.json()[activity_name]["max_participants"]
        
        # Add students up to capacity
        slots_available = max_capacity - initial_count
        for i in range(slots_available):
            email = f"student{i}@mergington.edu"
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify all students were added
        response = client.get("/activities")
        final_count = len(response.json()[activity_name]["participants"])
        assert final_count == max_capacity


class TestConcurrentOperations:
    """Integration tests for concurrent-like operations"""
    
    def test_multiple_signups_and_unregisters(self, client):
        """Test handling multiple signups and unregisters in sequence"""
        activity_name = "Drama Club"
        emails = [
            "actor1@mergington.edu",
            "actor2@mergington.edu",
            "actor3@mergington.edu"
        ]
        
        # Get initial state
        response = client.get("/activities")
        initial_participants = response.json()[activity_name]["participants"].copy()
        
        # Sign up all students
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Unregister some students
        for email in emails[:2]:
            response = client.delete(
                f"/activities/{activity_name}/unregister",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify final state
        response = client.get("/activities")
        final_participants = response.json()[activity_name]["participants"]
        
        assert emails[0] not in final_participants
        assert emails[1] not in final_participants
        assert emails[2] in final_participants


class TestErrorRecovery:
    """Integration tests for error handling and recovery"""
    
    def test_failed_signup_does_not_affect_activity_state(self, client):
        """Test that a failed signup doesn't corrupt activity data"""
        activity_name = "Chess Club"
        
        # Get initial state
        response = client.get("/activities")
        initial_state = response.json()[activity_name].copy()
        
        # Attempt invalid signup (duplicate)
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "michael@mergington.edu"}  # Already exists
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify state unchanged
        response = client.get("/activities")
        final_state = response.json()[activity_name]
        assert final_state == initial_state
    
    def test_failed_unregister_does_not_affect_activity_state(self, client):
        """Test that a failed unregister doesn't corrupt activity data"""
        activity_name = "Soccer Team"
        
        # Get initial state
        response = client.get("/activities")
        initial_state = response.json()[activity_name].copy()
        
        # Attempt invalid unregister (not signed up)
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": "notsignedup@mergington.edu"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify state unchanged
        response = client.get("/activities")
        final_state = response.json()[activity_name]
        assert final_state == initial_state


class TestDataConsistency:
    """Integration tests for data consistency"""
    
    def test_activity_data_persists_across_requests(self, client):
        """Test that activity data remains consistent across multiple requests"""
        email = "consistent@mergington.edu"
        activity_name = "Basketball Team"
        
        # Signup
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Make multiple GET requests to verify consistency
        for _ in range(5):
            response = client.get("/activities")
            assert response.status_code == status.HTTP_200_OK
            assert email in response.json()[activity_name]["participants"]
    
    def test_all_activities_maintain_structure(self, client):
        """Test that all activities maintain correct data structure"""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"{activity_name} missing {field}"
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)


class TestEdgeCases:
    """Integration tests for edge cases and boundary conditions"""
    
    def test_signup_unregister_signup_again(self, client):
        """Test that a student can signup, unregister, and signup again"""
        email = "indecisive@mergington.edu"
        activity_name = "Art Club"
        
        # First signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Unregister
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Signup again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify final state
        response = client.get("/activities")
        assert email in response.json()[activity_name]["participants"]
    
    def test_operations_on_all_activities(self, client):
        """Test that operations work correctly on all available activities"""
        response = client.get("/activities")
        all_activities = response.json()
        
        email = "explorer@mergington.edu"
        
        # Try signing up for each activity
        for activity_name in all_activities.keys():
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify enrolled in all
        response = client.get("/activities")
        updated_activities = response.json()
        for activity_name in all_activities.keys():
            assert email in updated_activities[activity_name]["participants"]
