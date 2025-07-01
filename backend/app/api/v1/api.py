from fastapi import APIRouter

from app.api.v1.endpoints import lists, login, users, calendars, list_items, votes, events

api_router = APIRouter()

# Include the login router
api_router.include_router(login.router, prefix="/login", tags=["login"])

# Include the users router  
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include the calendars router
api_router.include_router(calendars.router, prefix="/calendars", tags=["calendars"])

# Include the lists router
api_router.include_router(lists.router, prefix="/lists", tags=["lists"])

# Include the list items router
api_router.include_router(list_items.router, prefix="/list-items", tags=["list-items"])

# Include the votes router
api_router.include_router(votes.router, prefix="/votes", tags=["votes"])

# Include the events router
api_router.include_router(events.router, prefix="/events", tags=["events"])
