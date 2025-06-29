import pytest
from app.schemas.list import ListBase, ListCreate, ListUpdate, List
from app.models.list import ListType


class TestListSchemas:
    """Test Pydantic schemas for List model."""

    def test_list_base_schema(self):
        """Test ListBase schema validation."""
        data = {
            "name": "Test List",
            "list_type": ListType.TODO,
            "calendar_id": 1
        }
        
        list_base = ListBase(**data)
        
        assert list_base.name == "Test List"
        assert list_base.list_type == ListType.TODO
        assert list_base.calendar_id == 1

    def test_list_create_schema(self):
        """Test ListCreate schema validation."""
        data = {
            "name": "New List",
            "list_type": ListType.PRIORITY,
            "calendar_id": 2
        }
        
        list_create = ListCreate(**data)
        
        assert list_create.name == "New List"
        assert list_create.list_type == ListType.PRIORITY
        assert list_create.calendar_id == 2

    def test_list_create_with_defaults(self):
        """Test ListCreate schema with default values."""
        data = {
            "name": "Default List",
            "calendar_id": 1
            # list_type should default to TODO
        }
        
        list_create = ListCreate(**data)
        
        assert list_create.name == "Default List"
        assert list_create.list_type == ListType.TODO
        assert list_create.calendar_id == 1

    def test_list_update_schema(self):
        """Test ListUpdate schema validation."""
        data = {
            "name": "Updated Name",
            "list_type": ListType.PRIORITY
        }
        
        list_update = ListUpdate(**data)
        
        assert list_update.name == "Updated Name"
        assert list_update.list_type == ListType.PRIORITY

    def test_list_update_partial(self):
        """Test ListUpdate schema with partial data."""
        # Only updating name
        data = {"name": "Only Name Updated"}
        list_update = ListUpdate(**data)
        
        assert list_update.name == "Only Name Updated"
        assert list_update.list_type is None
        
        # Only updating list_type
        data = {"list_type": ListType.PRIORITY}
        list_update = ListUpdate(**data)
        
        assert list_update.name is None
        assert list_update.list_type == ListType.PRIORITY

    def test_list_update_empty(self):
        """Test ListUpdate schema with no data."""
        list_update = ListUpdate()
        
        assert list_update.name is None
        assert list_update.list_type is None

    def test_list_response_schema(self):
        """Test List response schema validation."""
        from datetime import datetime
        
        data = {
            "id": 1,
            "name": "Response List",
            "list_type": ListType.TODO,
            "calendar_id": 1,
            "created_at": datetime.now()
        }
        
        list_response = List(**data)
        
        assert list_response.id == 1
        assert list_response.name == "Response List"
        assert list_response.list_type == ListType.TODO
        assert list_response.calendar_id == 1
        assert list_response.created_at is not None

    def test_schema_validation_errors(self):
        """Test schema validation with invalid data."""
        # Missing required fields
        with pytest.raises(ValueError):
            ListCreate(name="Test")  # Missing calendar_id
        
        # Invalid types
        with pytest.raises(ValueError):
            ListCreate(
                name="Test",
                list_type="INVALID_TYPE",  # Invalid enum value
                calendar_id=1
            )
        
        with pytest.raises(ValueError):
            ListCreate(
                name="Test",
                list_type=ListType.TODO,
                calendar_id="invalid"  # Should be int
            )

    def test_schema_serialization(self):
        """Test schema serialization to dict."""
        list_create = ListCreate(
            name="Serialization Test",
            list_type=ListType.PRIORITY,
            calendar_id=1
        )
        
        data = list_create.model_dump()
        
        assert data["name"] == "Serialization Test"
        assert data["list_type"] == ListType.PRIORITY
        assert data["calendar_id"] == 1

    def test_schema_json_serialization(self):
        """Test schema JSON serialization."""
        list_create = ListCreate(
            name="JSON Test",
            list_type=ListType.TODO,
            calendar_id=1
        )
        
        json_str = list_create.model_dump_json()
        
        assert "JSON Test" in json_str
        assert "TODO" in json_str
        assert "1" in json_str
