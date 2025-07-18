import pytest
from fastapi.testclient import TestClient

from app.models.list import ListType


class TestListAPI:
    """Test API endpoints for List operations."""

    def test_create_list_endpoint(self, authenticated_client: TestClient):
        """Test POST /api/v1/lists/ endpoint."""
        list_data = {
            "name": "API Test List",
            "list_type": "TODO",
            "calendar_id": 1
        }
        
        response = authenticated_client.post("/api/v1/lists/", json=list_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "API Test List"
        assert data["list_type"] == "TODO"
        assert data["calendar_id"] == 1
        assert "id" in data
        assert "created_at" in data

    def test_get_lists_endpoint(self, authenticated_client: TestClient):
        """Test GET /api/v1/lists/ endpoint."""
        # Create a list first
        list_data = {
            "name": "Test List for Get",
            "list_type": "PRIORITY",
            "calendar_id": 2
        }
        authenticated_client.post("/api/v1/lists/", json=list_data)
        
        # Get all lists
        response = authenticated_client.get("/api/v1/lists/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(item["name"] == "Test List for Get" for item in data)

    def test_get_list_by_id_endpoint(self, authenticated_client: TestClient):
        """Test GET /api/v1/lists/{list_id} endpoint."""
        # Create a list first
        list_data = {
            "name": "Test List by ID",
            "list_type": "TODO",
            "calendar_id": 1
        }
        create_response = authenticated_client.post("/api/v1/lists/", json=list_data)
        created_list = create_response.json()
        list_id = created_list["id"]
        
        # Get the specific list
        response = authenticated_client.get(f"/api/v1/lists/{list_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == list_id
        assert data["name"] == "Test List by ID"

    def test_get_list_by_id_not_found(self, authenticated_client: TestClient):
        """Test GET /api/v1/lists/{list_id} with non-existent ID."""
        response = authenticated_client.get("/api/v1/lists/999")
        
        assert response.status_code == 404
        assert "List not found" in response.json()["detail"]

    def test_get_lists_by_calendar_endpoint(self, authenticated_client: TestClient):
        """Test GET /api/v1/lists/calendar/{calendar_id} endpoint."""
        # Create lists for different calendars
        list_data_1 = {
            "name": "Calendar 1 List 1", 
            "list_type": "TODO",
            "calendar_id": 1
        }
        list_data_2 = {
            "name": "Calendar 1 List 2",
            "list_type": "PRIORITY",
            "calendar_id": 1
        }
        list_data_3 = {
            "name": "Calendar 2 List",
            "list_type": "TODO",
            "calendar_id": 2
        }
        
        authenticated_client.post("/api/v1/lists/", json=list_data_1)
        authenticated_client.post("/api/v1/lists/", json=list_data_2)
        authenticated_client.post("/api/v1/lists/", json=list_data_3)
        
        # Get lists for calendar 1
        response = authenticated_client.get("/api/v1/lists/calendar/1")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert all(item["calendar_id"] == 1 for item in data)

    def test_update_list_endpoint(self, authenticated_client: TestClient):
        """Test PUT /api/v1/lists/{list_id} endpoint."""
        # Create a list first
        list_data = {
            "name": "Original Name",
            "list_type": "TODO",
            "calendar_id": 1
        }
        create_response = authenticated_client.post("/api/v1/lists/", json=list_data)
        created_list = create_response.json()
        list_id = created_list["id"]
        
        # Update the list
        update_data = {
            "name": "Updated Name",
            "list_type": "PRIORITY"
        }
        response = authenticated_client.put(f"/api/v1/lists/{list_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == list_id
        assert data["name"] == "Updated Name"
        assert data["list_type"] == "PRIORITY"
        assert data["calendar_id"] == 1  # Should remain unchanged

    def test_update_list_not_found(self, authenticated_client: TestClient):
        """Test PUT /api/v1/lists/{list_id} with non-existent ID."""
        update_data = {
            "name": "Updated Name",
            "list_type": "PRIORITY"
        }
        response = authenticated_client.put("/api/v1/lists/999", json=update_data)
        
        assert response.status_code == 404
        assert "List not found" in response.json()["detail"]

    def test_delete_list_endpoint(self, authenticated_client: TestClient):
        """Test DELETE /api/v1/lists/{list_id} endpoint."""
        # Create a list first
        list_data = {
            "name": "List to Delete",
            "list_type": "TODO",
            "calendar_id": 1
        }
        create_response = authenticated_client.post("/api/v1/lists/", json=list_data)
        created_list = create_response.json()
        list_id = created_list["id"]
        
        # Delete the list
        response = authenticated_client.delete(f"/api/v1/lists/{list_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == list_id
        assert data["name"] == "List to Delete"
        
        # Verify it's deleted
        get_response = authenticated_client.get(f"/api/v1/lists/{list_id}")
        assert get_response.status_code == 404

    def test_delete_list_not_found(self, authenticated_client: TestClient):
        """Test DELETE /api/v1/lists/{list_id} with non-existent ID."""
        response = authenticated_client.delete("/api/v1/lists/999")
        
        assert response.status_code == 404
        assert "List not found" in response.json()["detail"]

    def test_create_list_invalid_data(self, authenticated_client: TestClient):
        """Test POST /api/v1/lists/ with invalid data."""
        invalid_data = {
            "name": "",  # Empty name should fail
            "list_type": "TODO",
            "calendar_id": "invalid"  # Invalid calendar_id type
        }
        
        response = authenticated_client.post("/api/v1/lists/", json=invalid_data)
        
        assert response.status_code == 422  # Validation error

    def test_create_list_invalid_enum(self, authenticated_client: TestClient):
        """Test POST /api/v1/lists/ with invalid enum value."""
        invalid_data = {
            "name": "Test List",
            "list_type": "INVALID_TYPE",  # Invalid enum value
            "calendar_id": 1
        }
        
        response = authenticated_client.post("/api/v1/lists/", json=invalid_data)
        
        assert response.status_code == 422  # Validation error


class TestListAPIUnauthorized:
    """Test API endpoints without authentication."""

    def test_create_list_unauthorized(self, client: TestClient):
        """Test POST /api/v1/lists/ without authentication."""
        list_data = {
            "name": "API Test List",
            "list_type": "TODO",
            "calendar_id": 1
        }
        
        response = client.post("/api/v1/lists/", json=list_data)
        assert response.status_code == 401

    def test_get_lists_unauthorized(self, client: TestClient):
        """Test GET /api/v1/lists/ without authentication."""
        response = client.get("/api/v1/lists/")
        assert response.status_code == 401

    def test_get_list_by_id_unauthorized(self, client: TestClient):
        """Test GET /api/v1/lists/{list_id} without authentication."""
        response = client.get("/api/v1/lists/1")
        assert response.status_code == 401

    def test_update_list_unauthorized(self, client: TestClient):
        """Test PUT /api/v1/lists/{list_id} without authentication."""
        update_data = {"name": "Updated Name"}
        response = client.put("/api/v1/lists/1", json=update_data)
        assert response.status_code == 401

    def test_delete_list_unauthorized(self, client: TestClient):
        """Test DELETE /api/v1/lists/{list_id} without authentication."""
        response = client.delete("/api/v1/lists/1")
        assert response.status_code == 401
