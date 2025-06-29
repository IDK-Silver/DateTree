from fastapi import APIRouter

from app.api.v1.endpoints import lists

api_router = APIRouter()

# Include the lists router
api_router.include_router(lists.router, prefix="/lists", tags=["lists"])
