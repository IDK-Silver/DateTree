import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.schemas.list_item import ListItemCreate, ListItemUpdate, ListItem
from app.schemas.vote import VoteCreate, Vote
from app.schemas.event import EventCreate, EventUpdate, Event


class TestListItemSchemas:
    """Test ListItem schemas validation."""

    def test_list_item_create_valid(self):
        """Test creating a valid ListItemCreate schema."""
        data = {
            "content": "Test task",
            "is_completed": False,
            "list_id": 1
        }
        item = ListItemCreate(**data)
        assert item.content == "Test task"
        assert item.is_completed is False
        assert item.list_id == 1

    def test_list_item_create_defaults(self):
        """Test ListItemCreate with default values."""
        data = {
            "content": "Test task",
            "list_id": 1
        }
        item = ListItemCreate(**data)
        assert item.is_completed is False  # Default value

    def test_list_item_create_missing_required(self):
        """Test ListItemCreate with missing required fields."""
        with pytest.raises(ValidationError):
            ListItemCreate(content="Test")  # Missing list_id
        
        with pytest.raises(ValidationError):
            ListItemCreate(list_id=1)  # Missing content

    def test_list_item_update_partial(self):
        """Test ListItemUpdate with partial data."""
        update = ListItemUpdate(content="Updated content")
        assert update.content == "Updated content"
        assert update.is_completed is None

    def test_list_item_update_empty(self):
        """Test ListItemUpdate with no data."""
        update = ListItemUpdate()
        assert update.content is None
        assert update.is_completed is None

    def test_list_item_response(self):
        """Test ListItem response schema."""
        data = {
            "id": 1,
            "content": "Test task",
            "is_completed": False,
            "list_id": 1,
            "creator_id": 123,
            "created_at": datetime.now(timezone.utc),
            "vote_count": 5
        }
        item = ListItem(**data)
        assert item.id == 1
        assert item.vote_count == 5


class TestVoteSchemas:
    """Test Vote schemas validation."""

    def test_vote_create_valid(self):
        """Test creating a valid VoteCreate schema."""
        vote = VoteCreate(list_item_id=1)
        assert vote.list_item_id == 1

    def test_vote_create_missing_required(self):
        """Test VoteCreate with missing required fields."""
        with pytest.raises(ValidationError):
            VoteCreate()  # Missing list_item_id

    def test_vote_response(self):
        """Test Vote response schema."""
        data = {
            "id": 1,
            "user_id": 123,
            "list_item_id": 456
        }
        vote = Vote(**data)
        assert vote.id == 1
        assert vote.user_id == 123
        assert vote.list_item_id == 456


class TestEventSchemas:
    """Test Event schemas validation."""

    def test_event_create_valid(self):
        """Test creating a valid EventCreate schema."""
        data = {
            "title": "Team Meeting",
            "description": "Weekly sync",
            "start_time": datetime.now(timezone.utc),
            "end_time": datetime.now(timezone.utc),
            "calendar_id": 1
        }
        event = EventCreate(**data)
        assert event.title == "Team Meeting"
        assert event.description == "Weekly sync"
        assert event.calendar_id == 1

    def test_event_create_without_optional(self):
        """Test EventCreate without optional fields."""
        data = {
            "title": "Quick Event",
            "start_time": datetime.now(timezone.utc),
            "calendar_id": 1
        }
        event = EventCreate(**data)
        assert event.description is None
        assert event.end_time is None

    def test_event_create_missing_required(self):
        """Test EventCreate with missing required fields."""
        with pytest.raises(ValidationError):
            EventCreate(
                title="Test",
                start_time=datetime.now(timezone.utc)
            )  # Missing calendar_id

    def test_event_update_partial(self):
        """Test EventUpdate with partial data."""
        update = EventUpdate(title="Updated Title")
        assert update.title == "Updated Title"
        assert update.description is None
        assert update.start_time is None
        assert update.end_time is None

    def test_event_update_times(self):
        """Test EventUpdate with time fields."""
        now = datetime.now(timezone.utc)
        update = EventUpdate(
            start_time=now,
            end_time=now
        )
        assert update.start_time == now
        assert update.end_time == now

    def test_event_response(self):
        """Test Event response schema."""
        data = {
            "id": 1,
            "title": "Event",
            "description": "Description",
            "start_time": datetime.now(timezone.utc),
            "end_time": datetime.now(timezone.utc),
            "calendar_id": 1,
            "creator_id": 123
        }
        event = Event(**data)
        assert event.id == 1
        assert event.creator_id == 123

    def test_datetime_serialization(self):
        """Test that datetime fields are properly serialized."""
        now = datetime.now(timezone.utc)
        event_data = {
            "title": "Test Event",
            "start_time": now,
            "calendar_id": 1
        }
        event = EventCreate(**event_data)
        
        # Convert to dict and back to ensure serialization works
        event_dict = event.model_dump()
        assert isinstance(event_dict["start_time"], datetime)
        
        # Test JSON serialization
        event_json = event.model_dump_json()
        assert isinstance(event_json, str)

    def test_invalid_datetime_format(self):
        """Test that invalid datetime formats are rejected."""
        with pytest.raises(ValidationError):
            EventCreate(
                title="Test",
                start_time="invalid-date",
                calendar_id=1
            )