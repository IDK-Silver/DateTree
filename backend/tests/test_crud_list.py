import pytest
from sqlalchemy.orm import Session

from app.crud.crud_list import list_crud
from app.schemas.list import ListCreate, ListUpdate
from app.models.list import ListType


class TestListCRUD:
    """Test CRUD operations for List model."""

    def test_create_list(self, db_session: Session):
        """Test creating a new list."""
        list_data = ListCreate(
            name="Test Todo List",
            list_type=ListType.TODO,
            calendar_id=1
        )
        
        created_list = list_crud.create(db=db_session, obj_in=list_data)
        
        assert created_list.name == "Test Todo List"
        assert created_list.list_type == ListType.TODO
        assert created_list.calendar_id == 1
        assert created_list.id is not None
        assert created_list.created_at is not None

    def test_get_list(self, db_session: Session):
        """Test retrieving a list by ID."""
        # Create a list first
        list_data = ListCreate(
            name="Test List for Get",
            list_type=ListType.PRIORITY,
            calendar_id=2
        )
        created_list = list_crud.create(db=db_session, obj_in=list_data)
        
        # Retrieve the list
        retrieved_list = list_crud.get(db=db_session, id=created_list.id)
        
        assert retrieved_list is not None
        assert retrieved_list.id == created_list.id
        assert retrieved_list.name == "Test List for Get"
        assert retrieved_list.list_type == ListType.PRIORITY

    def test_get_list_not_found(self, db_session: Session):
        """Test retrieving a non-existent list."""
        retrieved_list = list_crud.get(db=db_session, id=999)
        assert retrieved_list is None

    def test_update_list(self, db_session: Session):
        """Test updating a list."""
        # Create a list first
        list_data = ListCreate(
            name="Original Name",
            list_type=ListType.TODO,
            calendar_id=1
        )
        created_list = list_crud.create(db=db_session, obj_in=list_data)
        
        # Update the list
        update_data = ListUpdate(
            name="Updated Name",
            list_type=ListType.PRIORITY
        )
        updated_list = list_crud.update(
            db=db_session, 
            db_obj=created_list, 
            obj_in=update_data
        )
        
        assert updated_list.name == "Updated Name"
        assert updated_list.list_type == ListType.PRIORITY
        assert updated_list.id == created_list.id

    def test_delete_list(self, db_session: Session):
        """Test deleting a list."""
        # Create a list first
        list_data = ListCreate(
            name="List to Delete",
            list_type=ListType.TODO,
            calendar_id=1
        )
        created_list = list_crud.create(db=db_session, obj_in=list_data)
        list_id = created_list.id
        
        # Delete the list
        deleted_list = list_crud.remove(db=db_session, id=list_id)
        
        assert deleted_list.id == list_id
        
        # Verify it's deleted
        retrieved_list = list_crud.get(db=db_session, id=list_id)
        assert retrieved_list is None

    def test_get_multi_lists(self, db_session: Session):
        """Test retrieving multiple lists."""
        # Create multiple lists
        for i in range(3):
            list_data = ListCreate(
                name=f"Test List {i}",
                list_type=ListType.TODO,
                calendar_id=1
            )
            list_crud.create(db=db_session, obj_in=list_data)
        
        # Retrieve all lists
        lists = list_crud.get_multi(db=db_session, skip=0, limit=10)
        
        assert len(lists) == 3
        assert all(list_obj.name.startswith("Test List") for list_obj in lists)

    def test_get_multi_by_calendar(self, db_session: Session):
        """Test retrieving lists by calendar ID."""
        # Create lists for different calendars
        calendar_1_lists = []
        for i in range(2):
            list_data = ListCreate(
                name=f"Calendar 1 List {i}",
                list_type=ListType.TODO,
                calendar_id=1
            )
            calendar_1_lists.append(list_crud.create(db=db_session, obj_in=list_data))
        
        # Create a list for calendar 2
        list_data = ListCreate(
            name="Calendar 2 List",
            list_type=ListType.PRIORITY,
            calendar_id=2
        )
        list_crud.create(db=db_session, obj_in=list_data)
        
        # Get lists for calendar 1
        calendar_1_retrieved = list_crud.get_multi_by_calendar(
            db=db_session, 
            calendar_id=1
        )
        
        assert len(calendar_1_retrieved) == 2
        assert all(list_obj.calendar_id == 1 for list_obj in calendar_1_retrieved)
        
        # Get lists for calendar 2
        calendar_2_retrieved = list_crud.get_multi_by_calendar(
            db=db_session, 
            calendar_id=2
        )
        
        assert len(calendar_2_retrieved) == 1
        assert calendar_2_retrieved[0].calendar_id == 2

    def test_get_by_calendar_and_type(self, db_session: Session):
        """Test retrieving lists by calendar and type."""
        # Create different types of lists for the same calendar
        todo_list = ListCreate(
            name="Todo List",
            list_type=ListType.TODO,
            calendar_id=1
        )
        priority_list = ListCreate(
            name="Priority List",
            list_type=ListType.PRIORITY,
            calendar_id=1
        )
        
        list_crud.create(db=db_session, obj_in=todo_list)
        list_crud.create(db=db_session, obj_in=priority_list)
        
        # Get TODO lists for calendar 1
        todo_lists = list_crud.get_by_calendar_and_type(
            db=db_session,
            calendar_id=1,
            list_type=ListType.TODO.value
        )
        
        assert len(todo_lists) == 1
        assert todo_lists[0].list_type == ListType.TODO
        
        # Get PRIORITY lists for calendar 1
        priority_lists = list_crud.get_by_calendar_and_type(
            db=db_session,
            calendar_id=1,
            list_type=ListType.PRIORITY.value
        )
        
        assert len(priority_lists) == 1
        assert priority_lists[0].list_type == ListType.PRIORITY
