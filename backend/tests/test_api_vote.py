import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.list_item import ListItemCreate


class TestVoteAPI:
    """Test API endpoints for Vote operations."""

    @pytest.fixture
    def test_list_item(self, db_session: Session, test_list: models.List, test_user: models.User) -> models.ListItem:
        """Create a test list item for voting tests."""
        item_data = ListItemCreate(
            content="Task to vote on",
            is_completed=False,
            list_id=test_list.id
        )
        # Create with user ID from test
        item = crud.list_item.create_with_user(
            db_session, 
            obj_in=item_data,
            creator_id=test_user.id
        )
        return item

    def test_create_vote(self, authenticated_client: TestClient, test_list_item: models.ListItem):
        """Test casting a vote on a list item."""
        vote_data = {
            "list_item_id": test_list_item.id
        }
        
        response = authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["list_item_id"] == test_list_item.id
        assert "id" in data
        assert "user_id" in data

    def test_duplicate_vote_prevention(self, authenticated_client: TestClient, test_list_item: models.ListItem):
        """Test that users cannot vote twice for the same item."""
        vote_data = {
            "list_item_id": test_list_item.id
        }
        
        # First vote should succeed
        response1 = authenticated_client.post("/api/v1/votes/", json=vote_data)
        assert response1.status_code == 200
        
        # Second vote should fail
        response2 = authenticated_client.post("/api/v1/votes/", json=vote_data)
        assert response2.status_code == 400
        assert response2.json()["detail"] == "User has already voted for this item"

    def test_get_votes_for_item(self, authenticated_client: TestClient, test_list_item: models.ListItem):
        """Test retrieving all votes for a specific item."""
        # Cast a vote
        vote_data = {"list_item_id": test_list_item.id}
        authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        # Get votes for item
        response = authenticated_client.get(f"/api/v1/votes/item/{test_list_item.id}")
        
        assert response.status_code == 200
        votes = response.json()
        assert len(votes) >= 1
        assert all(vote["list_item_id"] == test_list_item.id for vote in votes)

    def test_get_my_votes(self, authenticated_client: TestClient, test_list: models.List):
        """Test retrieving all votes by the current user."""
        # Create multiple items and vote on them
        for i in range(3):
            item_data = {
                "content": f"Task {i+1}",
                "list_id": test_list.id
            }
            item_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
            item_id = item_response.json()["id"]
            
            vote_data = {"list_item_id": item_id}
            authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        # Get my votes
        response = authenticated_client.get("/api/v1/votes/user/my-votes")
        
        assert response.status_code == 200
        votes = response.json()
        assert len(votes) == 3

    def test_remove_vote(self, authenticated_client: TestClient, test_list_item: models.ListItem):
        """Test removing a vote from a list item."""
        # Cast a vote
        vote_data = {"list_item_id": test_list_item.id}
        authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        # Remove vote
        response = authenticated_client.delete(f"/api/v1/votes/item/{test_list_item.id}")
        
        assert response.status_code == 200
        assert response.json()["message"] == "Vote removed successfully"
        
        # Verify removal - should be able to vote again
        vote_response = authenticated_client.post("/api/v1/votes/", json=vote_data)
        assert vote_response.status_code == 200

    def test_remove_nonexistent_vote(self, authenticated_client: TestClient, test_list_item: models.ListItem):
        """Test removing a vote that doesn't exist."""
        response = authenticated_client.delete(f"/api/v1/votes/item/{test_list_item.id}")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Vote not found"

    def test_vote_on_nonexistent_item(self, authenticated_client: TestClient):
        """Test voting on a non-existent list item."""
        vote_data = {
            "list_item_id": 999999
        }
        
        response = authenticated_client.post("/api/v1/votes/", json=vote_data)
        # Now properly validates list item existence in application layer
        assert response.status_code == 404
        assert "List item not found" in response.json()["detail"]

    def test_vote_counting_integration(self, authenticated_client: TestClient, test_list: models.List):
        """Test that vote counts are correctly reflected in list item queries."""
        # Create an item
        item_data = {
            "content": "Popular task",
            "list_id": test_list.id
        }
        item_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
        item_id = item_response.json()["id"]
        
        # Check initial vote count
        response1 = authenticated_client.get(f"/api/v1/list-items/list/{test_list.id}/with-votes")
        assert response1.json()[0]["vote_count"] == 0
        
        # Cast a vote
        vote_data = {"list_item_id": item_id}
        authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        # Check updated vote count
        response2 = authenticated_client.get(f"/api/v1/list-items/list/{test_list.id}/with-votes")
        assert response2.json()[0]["vote_count"] == 1

    def test_unauthorized_voting(self, client: TestClient, test_list_item: models.ListItem):
        """Test that unauthenticated users cannot vote."""
        vote_data = {
            "list_item_id": test_list_item.id
        }
        
        response = client.post("/api/v1/votes/", json=vote_data)
        assert response.status_code == 401

    def test_pagination_votes(self, authenticated_client: TestClient, test_list: models.List):
        """Test pagination of votes."""
        # Create many items and vote on them
        item_ids = []
        for i in range(10):
            item_data = {
                "content": f"Task {i+1}",
                "list_id": test_list.id
            }
            item_response = authenticated_client.post("/api/v1/list-items/", json=item_data)
            item_id = item_response.json()["id"]
            item_ids.append(item_id)
            
            vote_data = {"list_item_id": item_id}
            authenticated_client.post("/api/v1/votes/", json=vote_data)
        
        # Test pagination on user votes
        response = authenticated_client.get("/api/v1/votes/user/my-votes?skip=2&limit=3")
        
        assert response.status_code == 200
        votes = response.json()
        assert len(votes) == 3

    def test_vote_removal_idempotency(self, authenticated_client: TestClient, test_list_item: models.ListItem):
        """Test that removing a vote multiple times is handled gracefully."""
        # Cast and remove vote
        vote_data = {"list_item_id": test_list_item.id}
        authenticated_client.post("/api/v1/votes/", json=vote_data)
        authenticated_client.delete(f"/api/v1/votes/item/{test_list_item.id}")
        
        # Try to remove again
        response = authenticated_client.delete(f"/api/v1/votes/item/{test_list_item.id}")
        assert response.status_code == 404