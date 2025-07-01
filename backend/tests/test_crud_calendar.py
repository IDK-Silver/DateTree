# backend/tests/test_crud_calendar.py
import pytest
from sqlalchemy.orm import Session

from app.crud.crud_calendar import calendar_crud
from app.schemas.calendar import CalendarCreate, CalendarUpdate
from app.models.user import User


class TestCalendarCRUD:
    """Test CRUD operations for Calendar model."""

    def test_create_calendar_with_owner(self, db_session: Session, test_user: User):
        """Test creating a new calendar with an owner."""
        calendar_data = CalendarCreate(
            name="Test Calendar",
            description="A test calendar"
        )
        
        created_calendar = calendar_crud.create_with_owner(
            db=db_session, obj_in=calendar_data, owner_id=test_user.id
        )
        
        assert created_calendar.name == "Test Calendar"
        assert created_calendar.description == "A test calendar"
        assert created_calendar.owner_id == test_user.id
        assert created_calendar.id is not None

    def test_get_calendar(self, db_session: Session, test_user: User):
        """Test retrieving a calendar by ID."""
        calendar_data = CalendarCreate(name="Get Test Calendar")
        created_calendar = calendar_crud.create_with_owner(
            db=db_session, obj_in=calendar_data, owner_id=test_user.id
        )
        
        retrieved_calendar = calendar_crud.get(db=db_session, id=created_calendar.id)
        
        assert retrieved_calendar is not None
        assert retrieved_calendar.id == created_calendar.id
        assert retrieved_calendar.name == "Get Test Calendar"

    def test_update_calendar(self, db_session: Session, test_user: User):
        """Test updating a calendar."""
        calendar_data = CalendarCreate(name="Original Name")
        created_calendar = calendar_crud.create_with_owner(
            db=db_session, obj_in=calendar_data, owner_id=test_user.id
        )
        
        update_data = CalendarUpdate(name="Updated Name", description="Updated Desc")
        updated_calendar = calendar_crud.update(
            db=db_session, db_obj=created_calendar, obj_in=update_data
        )
        
        assert updated_calendar.name == "Updated Name"
        assert updated_calendar.description == "Updated Desc"

    def test_delete_calendar(self, db_session: Session, test_user: User):
        """Test deleting a calendar."""
        calendar_data = CalendarCreate(name="To Be Deleted")
        created_calendar = calendar_crud.create_with_owner(
            db=db_session, obj_in=calendar_data, owner_id=test_user.id
        )
        calendar_id = created_calendar.id
        
        deleted_calendar = calendar_crud.remove(db=db_session, id=calendar_id)
        
        assert deleted_calendar.id == calendar_id
        assert calendar_crud.get(db=db_session, id=calendar_id) is None

    def test_get_multi_by_owner(self, db_session: Session, test_user: User):
        """Test retrieving multiple calendars for a specific owner."""
        for i in range(3):
            calendar_crud.create_with_owner(
                db=db_session, 
                obj_in=CalendarCreate(name=f"Owner's Calendar {i}"), 
                owner_id=test_user.id
            )
        
        # Create a calendar for another user for noise
        # In a real scenario, you'd create another user
        calendar_crud.create_with_owner(
            db=db_session, 
            obj_in=CalendarCreate(name="Another User's Calendar"), 
            owner_id=999
        )

        calendars = calendar_crud.get_multi_by_owner(db=db_session, owner_id=test_user.id)
        
        assert len(calendars) == 5  # 3 created in test + 1 personal + 1 test calendar from fixtures
        assert all(c.owner_id == test_user.id for c in calendars)
