import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.schemas.event import EventCreate


class TestEventAPI:
    """Test API endpoints for Event operations."""

    def test_create_event(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test creating a new event."""
        event_data = {
            "title": "Team Meeting",
            "description": "Weekly team sync",
            "start_time": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            "end_time": (datetime.now(timezone.utc) + timedelta(days=1, hours=1)).isoformat(),
            "calendar_id": test_calendar.id
        }
        
        response = authenticated_client.post("/api/v1/events/", json=event_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == event_data["title"]
        assert data["description"] == event_data["description"]
        assert data["calendar_id"] == event_data["calendar_id"]
        assert "id" in data
        assert "creator_id" in data

    def test_create_event_without_end_time(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test creating an event without end time."""
        event_data = {
            "title": "Reminder",
            "description": "Quick reminder",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "calendar_id": test_calendar.id
        }
        
        response = authenticated_client.post("/api/v1/events/", json=event_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["end_time"] is None

    def test_get_events_by_calendar(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test retrieving all events for a calendar."""
        # Create multiple events
        base_time = datetime.now(timezone.utc)
        for i in range(3):
            event_data = {
                "title": f"Event {i+1}",
                "start_time": (base_time + timedelta(days=i)).isoformat(),
                "calendar_id": test_calendar.id
            }
            authenticated_client.post("/api/v1/events/", json=event_data)
        
        # Get events
        response = authenticated_client.get(f"/api/v1/events/calendar/{test_calendar.id}")
        
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 3
        assert all(event["calendar_id"] == test_calendar.id for event in events)

    def test_get_upcoming_events(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test retrieving upcoming events."""
        now = datetime.now(timezone.utc)
        
        # Create past and future events
        past_event = {
            "title": "Past Event",
            "start_time": (now - timedelta(days=1)).isoformat(),
            "calendar_id": test_calendar.id
        }
        future_event1 = {
            "title": "Future Event 1",
            "start_time": (now + timedelta(hours=1)).isoformat(),
            "calendar_id": test_calendar.id
        }
        future_event2 = {
            "title": "Future Event 2",
            "start_time": (now + timedelta(days=1)).isoformat(),
            "calendar_id": test_calendar.id
        }
        
        authenticated_client.post("/api/v1/events/", json=past_event)
        authenticated_client.post("/api/v1/events/", json=future_event1)
        authenticated_client.post("/api/v1/events/", json=future_event2)
        
        # Get upcoming events
        response = authenticated_client.get(f"/api/v1/events/calendar/{test_calendar.id}/upcoming")
        
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 2
        assert events[0]["title"] == "Future Event 1"  # Should be ordered by time
        assert events[1]["title"] == "Future Event 2"

    def test_get_upcoming_events_with_custom_time(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test retrieving upcoming events from a specific time."""
        base_time = datetime.now(timezone.utc)
        
        # Create events
        for i in range(5):
            event_data = {
                "title": f"Event {i+1}",
                "start_time": (base_time + timedelta(days=i)).isoformat(),
                "calendar_id": test_calendar.id
            }
            authenticated_client.post("/api/v1/events/", json=event_data)
        
        # Get events from day 2 onwards
        from_time = (base_time + timedelta(days=2)).isoformat()
        response = authenticated_client.get(
            f"/api/v1/events/calendar/{test_calendar.id}/upcoming",
            params={"from_time": from_time}
        )
        
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 3  # Events 3, 4, 5

    def test_get_events_by_date_range(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test retrieving events within a date range."""
        base_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Create events across a week
        for i in range(7):
            event_data = {
                "title": f"Day {i+1} Event",
                "start_time": (base_time + timedelta(days=i, hours=10)).isoformat(),
                "calendar_id": test_calendar.id
            }
            authenticated_client.post("/api/v1/events/", json=event_data)
        
        # Query for mid-week events (days 2-4)
        start_date = (base_time + timedelta(days=2)).isoformat()
        end_date = (base_time + timedelta(days=4, hours=23, minutes=59)).isoformat()
        
        response = authenticated_client.get(
            f"/api/v1/events/calendar/{test_calendar.id}/date-range",
            params={"start_date": start_date, "end_date": end_date}
        )
        
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 3  # Days 3, 4, 5
        assert events[0]["title"] == "Day 3 Event"
        assert events[2]["title"] == "Day 5 Event"

    def test_get_single_event(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test retrieving a single event by ID."""
        event_data = {
            "title": "Single Event",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "calendar_id": test_calendar.id
        }
        create_response = authenticated_client.post("/api/v1/events/", json=event_data)
        event_id = create_response.json()["id"]
        
        response = authenticated_client.get(f"/api/v1/events/{event_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == event_id
        assert data["title"] == "Single Event"

    def test_get_nonexistent_event(self, authenticated_client: TestClient):
        """Test getting a non-existent event returns 404."""
        response = authenticated_client.get("/api/v1/events/999999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"

    def test_update_event(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test updating an event."""
        # Create event
        event_data = {
            "title": "Original Event",
            "description": "Original description",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "calendar_id": test_calendar.id
        }
        create_response = authenticated_client.post("/api/v1/events/", json=event_data)
        event_id = create_response.json()["id"]
        
        # Update event
        update_data = {
            "title": "Updated Event",
            "description": "Updated description",
            "start_time": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
        }
        response = authenticated_client.put(f"/api/v1/events/{event_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Event"
        assert data["description"] == "Updated description"

    def test_update_event_time_range(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test updating event time range."""
        # Create event
        start_time = datetime.now(timezone.utc)
        event_data = {
            "title": "Time Range Event",
            "start_time": start_time.isoformat(),
            "end_time": (start_time + timedelta(hours=1)).isoformat(),
            "calendar_id": test_calendar.id
        }
        create_response = authenticated_client.post("/api/v1/events/", json=event_data)
        event_id = create_response.json()["id"]
        
        # Update times
        new_start = start_time + timedelta(days=1)
        update_data = {
            "start_time": new_start.isoformat(),
            "end_time": (new_start + timedelta(hours=2)).isoformat()
        }
        response = authenticated_client.put(f"/api/v1/events/{event_id}", json=update_data)
        
        assert response.status_code == 200

    def test_delete_event(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test deleting an event."""
        # Create event
        event_data = {
            "title": "Event to Delete",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "calendar_id": test_calendar.id
        }
        create_response = authenticated_client.post("/api/v1/events/", json=event_data)
        event_id = create_response.json()["id"]
        
        # Delete event
        response = authenticated_client.delete(f"/api/v1/events/{event_id}")
        
        assert response.status_code == 200
        
        # Verify deletion
        get_response = authenticated_client.get(f"/api/v1/events/{event_id}")
        assert get_response.status_code == 404

    def test_invalid_date_range(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test creating event with end time before start time (currently allowed)."""
        event_data = {
            "title": "Invalid Event",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
            "calendar_id": test_calendar.id
        }
        
        response = authenticated_client.post("/api/v1/events/", json=event_data)
        # Note: Currently no validation for end_time < start_time
        assert response.status_code == 200

    def test_pagination_events(self, authenticated_client: TestClient, test_calendar: models.Calendar):
        """Test pagination of events."""
        # Create many events
        base_time = datetime.now(timezone.utc)
        for i in range(10):
            event_data = {
                "title": f"Event {i+1}",
                "start_time": (base_time + timedelta(hours=i)).isoformat(),
                "calendar_id": test_calendar.id
            }
            authenticated_client.post("/api/v1/events/", json=event_data)
        
        # Test pagination
        response = authenticated_client.get(
            f"/api/v1/events/calendar/{test_calendar.id}?skip=3&limit=4"
        )
        
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 4

    def test_unauthorized_access(self, client: TestClient, test_calendar: models.Calendar):
        """Test that unauthenticated requests are rejected."""
        event_data = {
            "title": "Unauthorized Event",
            "start_time": datetime.now(timezone.utc).isoformat(),
            "calendar_id": test_calendar.id
        }
        
        response = client.post("/api/v1/events/", json=event_data)
        assert response.status_code == 401