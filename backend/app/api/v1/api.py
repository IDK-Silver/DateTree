from fastapi import APIRouter

from app.api.v1.endpoints import lists, login, users

api_router = APIRouter()

# Include the login router
api_router.include_router(login.router, tags=["login"])

# Include the users router  
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include the lists router
api_router.include_router(lists.router, prefix="/lists", tags=["lists"])
