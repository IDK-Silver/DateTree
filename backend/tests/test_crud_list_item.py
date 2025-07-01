import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.list_item import ListItemCreate, ListItemUpdate


class TestCRUDListItem:
    """Test CRUD operations for ListItem."""

    def test_create_list_item(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test creating a list item."""
        item_data = ListItemCreate(
            content="Test task",
            is_completed=False,
            list_id=test_list.id
        )
        
        item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        
        assert item.content == item_data.content
        assert item.is_completed == item_data.is_completed
        assert item.list_id == item_data.list_id
        assert item.creator_id == test_user.id
        assert item.id is not None

    def test_get_list_item(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test retrieving a list item by ID."""
        # Create item
        item_data = ListItemCreate(
            content="Get test item",
            list_id=test_list.id
        )
        created_item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        
        # Get item
        retrieved_item = crud.list_item.get(db_session, id=created_item.id)
        
        assert retrieved_item is not None
        assert retrieved_item.id == created_item.id
        assert retrieved_item.content == created_item.content

    def test_get_nonexistent_list_item(self, db_session: Session):
        """Test retrieving a non-existent list item returns None."""
        item = crud.list_item.get(db_session, id=999999)
        assert item is None

    def test_get_multi_by_list(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test retrieving multiple items by list."""
        # Create multiple items
        for i in range(5):
            item_data = ListItemCreate(
                content=f"Task {i+1}",
                is_completed=i % 2 == 0,
                list_id=test_list.id
            )
            crud.list_item.create_with_user(
                db_session,
                obj_in=item_data,
                creator_id=test_user.id
            )
        
        # Get items
        items = crud.list_item.get_multi_by_list(
            db_session,
            list_id=test_list.id,
            skip=0,
            limit=10
        )
        
        assert len(items) == 5
        assert all(item.list_id == test_list.id for item in items)

    def test_get_with_vote_count(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test retrieving list item with vote count."""
        # Create item
        item_data = ListItemCreate(
            content="Votable item",
            list_id=test_list.id
        )
        item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        
        # Create votes
        from app.schemas.vote import VoteCreate
        vote_data = VoteCreate(list_item_id=item.id)
        crud.vote.create_with_user(db_session, obj_in=vote_data, user_id=test_user.id)
        
        # Get item with vote count
        result = crud.list_item.get_with_vote_count(db_session, list_item_id=item.id)
        
        assert result is not None
        item_with_count, vote_count = result
        assert item_with_count.id == item.id
        assert vote_count == 1

    def test_get_multi_with_vote_counts(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test retrieving multiple items with vote counts."""
        # Create items
        items = []
        for i in range(3):
            item_data = ListItemCreate(
                content=f"Item {i+1}",
                list_id=test_list.id
            )
            item = crud.list_item.create_with_user(
                db_session,
                obj_in=item_data,
                creator_id=test_user.id
            )
            items.append(item)
        
        # Add votes to the second item
        from app.schemas.vote import VoteCreate
        vote_data = VoteCreate(list_item_id=items[1].id)
        crud.vote.create_with_user(db_session, obj_in=vote_data, user_id=test_user.id)
        
        # Get items with vote counts
        results = crud.list_item.get_multi_with_vote_counts(
            db_session,
            list_id=test_list.id
        )
        
        assert len(results) == 3
        # Check vote counts
        vote_counts = {item.id: count for item, count in results}
        assert vote_counts[items[0].id] == 0
        assert vote_counts[items[1].id] == 1
        assert vote_counts[items[2].id] == 0

    def test_update_list_item(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test updating a list item."""
        # Create item
        item_data = ListItemCreate(
            content="Original content",
            is_completed=False,
            list_id=test_list.id
        )
        item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        
        # Update item
        update_data = ListItemUpdate(
            content="Updated content",
            is_completed=True
        )
        updated_item = crud.list_item.update(
            db_session,
            db_obj=item,
            obj_in=update_data
        )
        
        assert updated_item.content == "Updated content"
        assert updated_item.is_completed is True
        assert updated_item.id == item.id

    def test_partial_update_list_item(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test partial update of a list item."""
        # Create item
        item_data = ListItemCreate(
            content="Original content",
            is_completed=False,
            list_id=test_list.id
        )
        item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        
        # Update only completion status
        update_data = ListItemUpdate(is_completed=True)
        updated_item = crud.list_item.update(
            db_session,
            db_obj=item,
            obj_in=update_data
        )
        
        assert updated_item.content == "Original content"  # Unchanged
        assert updated_item.is_completed is True  # Changed

    def test_delete_list_item(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test deleting a list item."""
        # Create item
        item_data = ListItemCreate(
            content="Item to delete",
            list_id=test_list.id
        )
        item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        item_id = item.id
        
        # Delete item
        deleted_item = crud.list_item.remove(db_session, id=item_id)
        
        assert deleted_item.id == item_id
        
        # Verify deletion
        retrieved_item = crud.list_item.get(db_session, id=item_id)
        assert retrieved_item is None

    def test_pagination(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test pagination of list items."""
        # Create many items
        for i in range(10):
            item_data = ListItemCreate(
                content=f"Task {i+1}",
                list_id=test_list.id
            )
            crud.list_item.create_with_user(
                db_session,
                obj_in=item_data,
                creator_id=test_user.id
            )
        
        # Test pagination
        page1 = crud.list_item.get_multi_by_list(
            db_session,
            list_id=test_list.id,
            skip=0,
            limit=3
        )
        page2 = crud.list_item.get_multi_by_list(
            db_session,
            list_id=test_list.id,
            skip=3,
            limit=3
        )
        
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].id != page2[0].id