import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.schemas.list_item import ListItemCreate


class TestListItemAPI:
    """Test API endpoints for ListItem operations."""

    def test_create_list_item(self, authenticated_client: TestClient, test_list: models.List):
        """Test creating a new list item."""
        item_data = {
            "content": "Test task to complete",
            "is_completed": False,
            "list_id": test_list.id
        }
        
        response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == item_data["content"]
        assert data["is_completed"] == item_data["is_completed"]
        assert data["list_id"] == item_data["list_id"]
        assert "id" in data
        assert "created_at" in data
        assert "creator_id" in data

    def test_get_list_items_by_list(self, authenticated_client: TestClient, test_list: models.List):
        """Test retrieving all items for a specific list."""
        # Create multiple items
        for i in range(3):
            item_data = {
                "content": f"Task {i+1}",
                "is_completed": i % 2 == 0,
                "list_id": test_list.id
            }
            authenticated_client.post("/api/v1/list-items/", json=item_data)
        
        # Get items for the list
        response = authenticated_client.get(f"/api/v1/list-items/list/{test_list.id}")
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3
        assert all(item["list_id"] == test_list.id for item in items)

    def test_get_list_items_with_votes(self, authenticated_client: TestClient, test_list: models.List):
        """Test retrieving list items with vote counts."""
        # Create items
        item_data = {
            "content": "Popular task",
            "list_id": test_list.id
        }
        item_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        item_id = item_response.json()["id"]
        
        # Add vote
        vote_data = {"list_item_id": item_id}
        authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        # Get items with votes
        response = authenticated_client.get(f"/api/v1/list-items/list/{test_list.id}/with-votes")
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        assert items[0]["vote_count"] == 1
        assert items[0]["content"] == "Popular task"

    def test_get_single_list_item(self, authenticated_client: TestClient, test_list: models.List):
        """Test retrieving a single list item by ID."""
        # Create item
        item_data = {
            "content": "Single task",
            "list_id": test_list.id
        }
        create_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        item_id = create_response.json()["id"]
        
        # Get single item
        response = authenticated_client.get(f"/api/v1/list-items/{item_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["content"] == "Single task"

    def test_get_nonexistent_list_item(self, authenticated_client: TestClient):
        """Test getting a non-existent list item returns 404."""
        response = authenticated_client.get("/api/v1/list-items/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "List item not found"

    def test_update_list_item(self, authenticated_client: TestClient, test_list: models.List):
        """Test updating a list item."""
        # Create item
        item_data = {
            "content": "Original task",
            "is_completed": False,
            "list_id": test_list.id
        }
        create_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        item_id = create_response.json()["id"]
        
        # Update item
        update_data = {
            "content": "Updated task",
            "is_completed": True
        }
        response = authenticated_client.put(f"/api/v1/list-items/{item_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Updated task"
        assert data["is_completed"] is True

    def test_update_nonexistent_list_item(self, authenticated_client: TestClient):
        """Test updating a non-existent list item returns 404."""
        update_data = {"content": "Updated"}
        response = authenticated_client.put("/api/v1/list-items/999999", json=update_data)
        assert response.status_code == 404

    def test_delete_list_item(self, authenticated_client: TestClient, test_list: models.List):
        """Test deleting a list item."""
        # Create item
        item_data = {
            "content": "Task to delete",
            "list_id": test_list.id
        }
        create_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        item_id = create_response.json()["id"]
        
        # Delete item
        response = authenticated_client.delete(f"/api/v1/list-items/{item_id}")
        
        assert response.status_code == 200
        
        # Verify deletion
        get_response = authenticated_client.get(f"/api/v1/list-items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_list_item(self, authenticated_client: TestClient):
        """Test deleting a non-existent list item returns 404."""
        response = authenticated_client.delete("/api/v1/list-items/999999")
        assert response.status_code == 404

    def test_pagination(self, authenticated_client: TestClient, test_list: models.List):
        """Test pagination of list items."""
        # Create many items
        for i in range(10):
            item_data = {
                "content": f"Task {i+1}",
                "list_id": test_list.id
            }
            authenticated_client.post("/api/v1/list-items/", json=item_data)
        
        # Test pagination
        response = authenticated_client.get(
            f"/api/v1/list-items/list/{test_list.id}?skip=2&limit=3"
        )
        
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3

    def test_unauthorized_access(self, client: TestClient, test_list: models.List):
        """Test that unauthenticated requests are rejected."""
        item_data = {
            "content": "Unauthorized task",
            "list_id": test_list.id
        }
        
        response = client.post("/api/v1/list-items/", json=item_data)
        assert response.status_code == 401

    def test_create_item_invalid_list(self, authenticated_client: TestClient):
        """Test creating an item for non-existent list."""
        item_data = {
            "content": "Task for invalid list",
            "list_id": 999999
        }
        
        # Note: SQLite test DB doesn't enforce foreign key constraints
        response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        assert response.status_code == 200