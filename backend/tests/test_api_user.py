# backend/tests/test_api_user.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate


class TestUserRegistration:
    """Test user registration endpoint."""
    
    def test_register_user_success(self, client: TestClient, db_session: Session):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert data["is_active"] is True
        assert "password" not in data
        assert "hashed_password" not in data
        
        # Verify user was created in database
        user = crud.user.get_by_email(db_session, email=user_data["email"])
        assert user is not None
        assert user.email == user_data["email"]
        assert user.is_active is True
    
    def test_register_user_duplicate_email(self, client: TestClient, test_user):
        """Test registration with existing email fails."""
        user_data = {
            "email": test_user.email,  # Use existing user's email
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "already exists" in data["detail"]
    
    def test_register_user_invalid_email(self, client: TestClient):
        """Test registration with invalid email format fails."""
        user_data = {
            "email": "invalid-email-format",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_register_user_missing_password(self, client: TestClient):
        """Test registration without password fails."""
        user_data = {
            "email": "test@example.com"
            # password missing
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_register_user_missing_email(self, client: TestClient):
        """Test registration without email fails."""
        user_data = {
            "password": "testpassword123"
            # email missing
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_register_user_empty_password(self, client: TestClient):
        """Test registration with empty password - currently allowed but creates security risk."""
        user_data = {
            "email": "emptypass@example.com",
            "password": ""
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        # Currently empty passwords are accepted - this test documents current behavior
        # TODO: In the future, you should add password validation to reject empty passwords
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        
    def test_register_user_weak_password_accepted(self, client: TestClient, db_session: Session):
        """Test that weak passwords are accepted (no password strength validation implemented yet)."""
        user_data = {
            "email": "weakpass@example.com",
            "password": "123"
        }
        
        response = client.post("/api/v1/users/register", json=user_data)
        
        # Currently we accept weak passwords - this test documents current behavior
        # In the future, you might want to add password strength validation
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        
        # Clean up
        user = crud.user.get_by_email(db_session, email=user_data["email"])
        if user:
            db_session.delete(user)
            db_session.commit()
