import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.vote import VoteCreate
from app.schemas.list_item import ListItemCreate


class TestCRUDVote:
    """Test CRUD operations for Vote."""

    @pytest.fixture
    def test_list_item(self, db_session: Session, test_list: models.List, test_user: models.User) -> models.ListItem:
        """Create a test list item for voting tests."""
        item_data = ListItemCreate(
            content="Task for voting",
            is_completed=False,
            list_id=test_list.id
        )
        item = crud.list_item.create_with_user(
            db_session,
            obj_in=item_data,
            creator_id=test_user.id
        )
        return item

    def test_create_vote(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test creating a vote."""
        vote_data = VoteCreate(list_item_id=test_list_item.id)
        
        vote = crud.vote.create_with_user(
            db_session,
            obj_in=vote_data,
            user_id=test_user.id
        )
        
        assert vote.list_item_id == test_list_item.id
        assert vote.user_id == test_user.id
        assert vote.id is not None

    def test_get_vote(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test retrieving a vote by ID."""
        # Create vote
        vote_data = VoteCreate(list_item_id=test_list_item.id)
        created_vote = crud.vote.create_with_user(
            db_session,
            obj_in=vote_data,
            user_id=test_user.id
        )
        
        # Get vote
        retrieved_vote = crud.vote.get(db_session, id=created_vote.id)
        
        assert retrieved_vote is not None
        assert retrieved_vote.id == created_vote.id
        assert retrieved_vote.user_id == test_user.id

    def test_get_by_user_and_item(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test retrieving a vote by user and item."""
        # Create vote
        vote_data = VoteCreate(list_item_id=test_list_item.id)
        crud.vote.create_with_user(
            db_session,
            obj_in=vote_data,
            user_id=test_user.id
        )
        
        # Get vote by user and item
        vote = crud.vote.get_by_user_and_item(
            db_session,
            user_id=test_user.id,
            list_item_id=test_list_item.id
        )
        
        assert vote is not None
        assert vote.user_id == test_user.id
        assert vote.list_item_id == test_list_item.id

    def test_get_by_user_and_item_not_found(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test retrieving a non-existent vote returns None."""
        vote = crud.vote.get_by_user_and_item(
            db_session,
            user_id=test_user.id,
            list_item_id=test_list_item.id
        )
        assert vote is None

    def test_get_multi_by_item(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test retrieving all votes for an item."""
        # Create additional users and votes
        from app.schemas.user import UserCreate
        
        users = []
        for i in range(3):
            user_data = UserCreate(
                email=f"voter{i}@example.com",
                password="password123"
            )
            user = crud.user.create(db_session, obj_in=user_data)
            users.append(user)
            
            vote_data = VoteCreate(list_item_id=test_list_item.id)
            crud.vote.create_with_user(
                db_session,
                obj_in=vote_data,
                user_id=user.id
            )
        
        # Get votes for item
        votes = crud.vote.get_multi_by_item(
            db_session,
            list_item_id=test_list_item.id
        )
        
        assert len(votes) == 3
        assert all(vote.list_item_id == test_list_item.id for vote in votes)

    def test_get_multi_by_user(self, db_session: Session, test_list: models.List, test_user: models.User):
        """Test retrieving all votes by a user."""
        # Create multiple items and vote on them
        items = []
        for i in range(3):
            item_data = ListItemCreate(
                content=f"Task {i+1}",
                list_id=test_list.id
            )
            item = crud.list_item.create_with_user(
                db_session,
                obj_in=item_data,
                creator_id=test_user.id
            )
            items.append(item)
            
            vote_data = VoteCreate(list_item_id=item.id)
            crud.vote.create_with_user(
                db_session,
                obj_in=vote_data,
                user_id=test_user.id
            )
        
        # Get votes by user
        votes = crud.vote.get_multi_by_user(
            db_session,
            user_id=test_user.id
        )
        
        assert len(votes) == 3
        assert all(vote.user_id == test_user.id for vote in votes)

    def test_remove_by_user_and_item(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test removing a vote by user and item."""
        # Create vote
        vote_data = VoteCreate(list_item_id=test_list_item.id)
        vote = crud.vote.create_with_user(
            db_session,
            obj_in=vote_data,
            user_id=test_user.id
        )
        vote_id = vote.id
        
        # Remove vote
        removed_vote = crud.vote.remove_by_user_and_item(
            db_session,
            user_id=test_user.id,
            list_item_id=test_list_item.id
        )
        
        assert removed_vote is not None
        assert removed_vote.id == vote_id
        
        # Verify removal
        vote_check = crud.vote.get(db_session, id=vote_id)
        assert vote_check is None

    def test_remove_by_user_and_item_not_found(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test removing a non-existent vote returns None."""
        removed_vote = crud.vote.remove_by_user_and_item(
            db_session,
            user_id=test_user.id,
            list_item_id=test_list_item.id
        )
        assert removed_vote is None

    def test_delete_vote(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test deleting a vote by ID."""
        # Create vote
        vote_data = VoteCreate(list_item_id=test_list_item.id)
        vote = crud.vote.create_with_user(
            db_session,
            obj_in=vote_data,
            user_id=test_user.id
        )
        vote_id = vote.id
        
        # Delete vote
        deleted_vote = crud.vote.remove(db_session, id=vote_id)
        
        assert deleted_vote.id == vote_id
        
        # Verify deletion
        vote_check = crud.vote.get(db_session, id=vote_id)
        assert vote_check is None

    def test_cascade_delete_with_list_item(self, db_session: Session, test_list_item: models.ListItem, test_user: models.User):
        """Test that votes are deleted when list item is deleted."""
        # Create vote
        vote_data = VoteCreate(list_item_id=test_list_item.id)
        vote = crud.vote.create_with_user(
            db_session,
            obj_in=vote_data,
            user_id=test_user.id
        )
        vote_id = vote.id
        
        # Delete list item
        crud.list_item.remove(db_session, id=test_list_item.id)
        
        # Vote should be deleted too
        vote_check = crud.vote.get(db_session, id=vote_id)
        assert vote_check is None

    def test_pagination_votes(self, db_session: Session, test_list_item: models.ListItem):
        """Test pagination of votes."""
        # Create many users and votes
        from app.schemas.user import UserCreate
        
        for i in range(10):
            user_data = UserCreate(
                email=f"paginationuser{i}@example.com",
                password="password123"
            )
            user = crud.user.create(db_session, obj_in=user_data)
            
            vote_data = VoteCreate(list_item_id=test_list_item.id)
            crud.vote.create_with_user(
                db_session,
                obj_in=vote_data,
                user_id=user.id
            )
        
        # Test pagination
        page1 = crud.vote.get_multi_by_item(
            db_session,
            list_item_id=test_list_item.id,
            skip=0,
            limit=3
        )
        page2 = crud.vote.get_multi_by_item(
            db_session,
            list_item_id=test_list_item.id,
            skip=3,
            limit=3
        )
        
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].id != page2[0].id