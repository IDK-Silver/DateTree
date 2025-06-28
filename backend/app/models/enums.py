import enum

class PermissionLevel(enum.Enum):
    """Define permission levels for calendar members"""
    VIEW_ONLY = "view_only"
    EDITOR = "editor"
    OWNER = "owner"

class EventStatus(enum.Enum):
    """Define event status"""
    TODO = "todo"
    COMPLETED = "completed"