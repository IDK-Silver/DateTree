import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app import crud, models
from app.schemas.event import EventCreate, EventUpdate


class TestCRUDEvent:
    """Test CRUD operations for Event."""

    def test_create_event(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test creating an event."""
        event_data = EventCreate(
            title="Test Event",
            description="Event description",
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc) + timedelta(hours=1),
            calendar_id=test_calendar.id
        )
        
        event = crud.event.create_with_user(
            db_session,
            obj_in=event_data,
            creator_id=test_user.id
        )
        
        assert event.title == event_data.title
        assert event.description == event_data.description
        assert event.calendar_id == event_data.calendar_id
        assert event.creator_id == test_user.id
        assert event.id is not None

    def test_create_event_without_end_time(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test creating an event without end time."""
        event_data = EventCreate(
            title="All-day Event",
            start_time=datetime.now(timezone.utc),
            calendar_id=test_calendar.id
        )
        
        event = crud.event.create_with_user(
            db_session,
            obj_in=event_data,
            creator_id=test_user.id
        )
        
        assert event.end_time is None

    def test_get_event(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test retrieving an event by ID."""
        # Create event
        event_data = EventCreate(
            title="Get Test Event",
            start_time=datetime.now(timezone.utc),
            calendar_id=test_calendar.id
        )
        created_event = crud.event.create_with_user(
            db_session,
            obj_in=event_data,
            creator_id=test_user.id
        )
        
        # Get event
        retrieved_event = crud.event.get(db_session, id=created_event.id)
        
        assert retrieved_event is not None
        assert retrieved_event.id == created_event.id
        assert retrieved_event.title == created_event.title

    def test_get_multi_by_calendar(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test retrieving multiple events by calendar."""
        # Create multiple events
        base_time = datetime.now(timezone.utc)
        for i in range(5):
            event_data = EventCreate(
                title=f"Event {i+1}",
                start_time=base_time + timedelta(days=i),
                calendar_id=test_calendar.id
            )
            crud.event.create_with_user(
                db_session,
                obj_in=event_data,
                creator_id=test_user.id
            )
        
        # Get events
        events = crud.event.get_multi_by_calendar(
            db_session,
            calendar_id=test_calendar.id,
            skip=0,
            limit=10
        )
        
        assert len(events) == 5
        assert all(event.calendar_id == test_calendar.id for event in events)

    def test_get_multi_by_date_range(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test retrieving events within a date range."""
        base_time = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Create events across a week
        for i in range(7):
            event_data = EventCreate(
                title=f"Day {i+1} Event",
                start_time=base_time + timedelta(days=i),
                calendar_id=test_calendar.id
            )
            crud.event.create_with_user(
                db_session,
                obj_in=event_data,
                creator_id=test_user.id
            )
        
        # Query for mid-week events
        start_date = base_time + timedelta(days=2)
        end_date = base_time + timedelta(days=4)
        
        events = crud.event.get_multi_by_date_range(
            db_session,
            calendar_id=test_calendar.id,
            start_date=start_date,
            end_date=end_date
        )
        
        assert len(events) == 3  # Days 2, 3, 4
        assert events[0].title == "Day 3 Event"
        assert events[2].title == "Day 5 Event"

    def test_get_upcoming_events(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test retrieving upcoming events."""
        now = datetime.now(timezone.utc)
        
        # Create past and future events
        past_event = EventCreate(
            title="Past Event",
            start_time=now - timedelta(days=1),
            calendar_id=test_calendar.id
        )
        future_event1 = EventCreate(
            title="Near Future Event",
            start_time=now + timedelta(hours=1),
            calendar_id=test_calendar.id
        )
        future_event2 = EventCreate(
            title="Far Future Event",
            start_time=now + timedelta(days=1),
            calendar_id=test_calendar.id
        )
        
        crud.event.create_with_user(db_session, obj_in=past_event, creator_id=test_user.id)
        crud.event.create_with_user(db_session, obj_in=future_event1, creator_id=test_user.id)
        crud.event.create_with_user(db_session, obj_in=future_event2, creator_id=test_user.id)
        
        # Get upcoming events
        events = crud.event.get_upcoming_events(
            db_session,
            calendar_id=test_calendar.id
        )
        
        assert len(events) == 2
        assert events[0].title == "Near Future Event"  # Ordered by start time
        assert events[1].title == "Far Future Event"

    def test_get_upcoming_events_custom_time(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test retrieving upcoming events from a specific time."""
        base_time = datetime.now(timezone.utc)
        
        # Create events
        for i in range(5):
            event_data = EventCreate(
                title=f"Event {i+1}",
                start_time=base_time + timedelta(days=i),
                calendar_id=test_calendar.id
            )
            crud.event.create_with_user(
                db_session,
                obj_in=event_data,
                creator_id=test_user.id
            )
        
        # Get events from day 2 onwards
        from_time = base_time + timedelta(days=2)
        events = crud.event.get_upcoming_events(
            db_session,
            calendar_id=test_calendar.id,
            from_time=from_time
        )
        
        assert len(events) == 3  # Events 3, 4, 5

    def test_update_event(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test updating an event."""
        # Create event
        event_data = EventCreate(
            title="Original Title",
            description="Original description",
            start_time=datetime.now(timezone.utc),
            calendar_id=test_calendar.id
        )
        event = crud.event.create_with_user(
            db_session,
            obj_in=event_data,
            creator_id=test_user.id
        )
        
        # Update event
        update_data = EventUpdate(
            title="Updated Title",
            description="Updated description"
        )
        updated_event = crud.event.update(
            db_session,
            db_obj=event,
            obj_in=update_data
        )
        
        assert updated_event.title == "Updated Title"
        assert updated_event.description == "Updated description"
        assert updated_event.id == event.id

    def test_update_event_times(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test updating event times."""
        # Create event
        start_time = datetime.now(timezone.utc)
        event_data = EventCreate(
            title="Time Update Event",
            start_time=start_time,
            end_time=start_time + timedelta(hours=1),
            calendar_id=test_calendar.id
        )
        event = crud.event.create_with_user(
            db_session,
            obj_in=event_data,
            creator_id=test_user.id
        )
        
        # Update times
        new_start = start_time + timedelta(days=1)
        update_data = EventUpdate(
            start_time=new_start,
            end_time=new_start + timedelta(hours=2)
        )
        updated_event = crud.event.update(
            db_session,
            db_obj=event,
            obj_in=update_data
        )
        
        # Compare without timezone since SQLite doesn't preserve timezone info
        assert updated_event.start_time.replace(tzinfo=timezone.utc) == new_start
        assert updated_event.end_time.replace(tzinfo=timezone.utc) == new_start + timedelta(hours=2)

    def test_delete_event(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test deleting an event."""
        # Create event
        event_data = EventCreate(
            title="Event to Delete",
            start_time=datetime.now(timezone.utc),
            calendar_id=test_calendar.id
        )
        event = crud.event.create_with_user(
            db_session,
            obj_in=event_data,
            creator_id=test_user.id
        )
        event_id = event.id
        
        # Delete event
        deleted_event = crud.event.remove(db_session, id=event_id)
        
        assert deleted_event.id == event_id
        
        # Verify deletion
        retrieved_event = crud.event.get(db_session, id=event_id)
        assert retrieved_event is None

    def test_pagination_events(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test pagination of events."""
        # Create many events
        base_time = datetime.now(timezone.utc)
        for i in range(10):
            event_data = EventCreate(
                title=f"Event {i+1}",
                start_time=base_time + timedelta(hours=i),
                calendar_id=test_calendar.id
            )
            crud.event.create_with_user(
                db_session,
                obj_in=event_data,
                creator_id=test_user.id
            )
        
        # Test pagination
        page1 = crud.event.get_multi_by_calendar(
            db_session,
            calendar_id=test_calendar.id,
            skip=0,
            limit=3
        )
        page2 = crud.event.get_multi_by_calendar(
            db_session,
            calendar_id=test_calendar.id,
            skip=3,
            limit=3
        )
        
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].id != page2[0].id

    def test_event_ordering(self, db_session: Session, test_calendar: models.Calendar, test_user: models.User):
        """Test that upcoming events are properly ordered by start time."""
        base_time = datetime.now(timezone.utc)
        
        # Create events in random order
        times = [
            base_time + timedelta(hours=3),
            base_time + timedelta(hours=1),
            base_time + timedelta(hours=5),
            base_time + timedelta(hours=2)
        ]
        
        for i, start_time in enumerate(times):
            event_data = EventCreate(
                title=f"Event at hour {i}",
                start_time=start_time,
                calendar_id=test_calendar.id
            )
            crud.event.create_with_user(
                db_session,
                obj_in=event_data,
                creator_id=test_user.id
            )
        
        # Get upcoming events
        events = crud.event.get_upcoming_events(
            db_session,
            calendar_id=test_calendar.id
        )
        
        # Verify ordering
        for i in range(len(events) - 1):
            assert events[i].start_time <= events[i + 1].start_time