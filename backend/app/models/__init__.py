# Import the Base so it's accessible from this package.
from .base import Base

# Import all the models so they are registered with SQLAlchemy's metadata.
# This is crucial for Alembic to detect the tables.
from .user import User
from .calendar import Calendar, calendar_user_association
from .list import List, ListType
from .list_item import ListItem
from .vote import Vote
from .event import Event

# You can also define a __all__ to control what `from .models import *` imports.
__all__ = [
    "Base",
    "User",
    "Calendar",
    "calendar_user_association",
    "List",
    "ListType",
    "ListItem",
    "Vote",
    "Event",
]