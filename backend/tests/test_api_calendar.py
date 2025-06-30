# backend/tests/test_api_calendar.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud.crud_calendar import calendar_crud
from app.schemas.calendar import CalendarCreate
from app.models.user import User


@pytest.fixture
def test_calendar(db_session: Session, test_user: User):
    """Create a test calendar for API tests."""
    calendar_data = CalendarCreate(name="My Test Calendar", description="API test desc")
    return calendar_crud.create_with_owner(
        db=db_session, obj_in=calendar_data, owner_id=test_user.id
    )

class TestCalendarAPI:
    """Test API endpoints for Calendar operations."""

    def test_create_calendar_endpoint(self, authenticated_client: TestClient):
        """Test POST /api/v1/calendars/ endpoint."""
        calendar_data = {"name": "API Test Calendar", "description": "Created via API"}
        
        response = authenticated_client.post("/api/v1/calendars/", json=calendar_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "API Test Calendar"
        assert data["description"] == "Created via API"
        assert "id" in data
        assert "owner" in data
        assert data["owner"]["email"] == "test@example.com"

    def test_get_calendars_endpoint(self, authenticated_client: TestClient, test_calendar):
        """Test GET /api/v1/calendars/ endpoint."""
        response = authenticated_client.get("/api/v1/calendars/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(item["name"] == test_calendar.name for item in data)

    def test_get_calendar_by_id_endpoint(self, authenticated_client: TestClient, test_calendar):
        """Test GET /api/v1/calendars/{calendar_id} endpoint."""
        response = authenticated_client.get(f"/api/v1/calendars/{test_calendar.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_calendar.id
        assert data["name"] == test_calendar.name

    def test_get_calendar_not_found(self, authenticated_client: TestClient):
        """Test GET non-existent calendar."""
        response = authenticated_client.get("/api/v1/calendars/999")
        assert response.status_code == 404

    def test_get_calendar_not_owner(self, client: TestClient, test_calendar, db_session: Session):
        """Test GET calendar belonging to another user."""
        # Create another user and token
        from app.schemas.user import UserCreate
        from app.core.security import create_access_token
        from app import crud
        other_user_data = UserCreate(email="other@example.com", password="password")
        other_user = crud.user.create(db_session, obj_in=other_user_data)
        other_token = create_access_token(subject=other_user.email)
        
        # Use the other user's token to try and access the calendar
        response = client.get(
            f"/api/v1/calendars/{test_calendar.id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        assert response.status_code == 403

    def test_update_calendar_endpoint(self, authenticated_client: TestClient, test_calendar):
        """Test PUT /api/v1/calendars/{calendar_id} endpoint."""
        update_data = {"name": "Updated Calendar Name"}
        
        response = authenticated_client.put(
            f"/api/v1/calendars/{test_calendar.id}", json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Calendar Name"
        assert data["id"] == test_calendar.id

    def test_delete_calendar_endpoint(self, authenticated_client: TestClient, test_calendar):
        """Test DELETE /api/v1/calendars/{calendar_id} endpoint."""
        response = authenticated_client.delete(f"/api/v1/calendars/{test_calendar.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_calendar.id
        
        # Verify it's deleted
        get_response = authenticated_client.get(f"/api/v1/calendars/{test_calendar.id}")
        assert get_response.status_code == 404
