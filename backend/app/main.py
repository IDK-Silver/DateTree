from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    ## DateTree - Collaborative Task and Event Management API

    DateTree is a modern collaborative task and event management system that supports team voting decisions and personal task tracking.

    ### Main Features

    * **User Management**: User registration, login, JWT authentication
    * **Calendar System**: Personal and shared calendar management
    * **List Management**: TODO and PRIORITY list types
    * **Task Tracking**: Completion status management for list items
    * **Collaborative Voting**: PRIORITY lists support team voting decisions
    * **Event Management**: Schedule planning and time management

    ### Data Structure

    ```
    User
    `-- Calendar [1:N]
        |-- List [1:N]
        |   `-- ListItem [1:N]
        |       `-- Vote [1:N]
        `-- Event [1:N]
    ```

    ### Getting Started

    1. **Register User**: Use `/api/v1/users/register` to create account
    2. **Login for Token**: Use `/api/v1/auth/login` to get authentication token
    3. **Create Calendar**: Personal calendar auto-created on registration, manually create project calendars
    4. **Manage Lists**: Create TODO or PRIORITY type lists in calendars
    5. **Collaborative Voting**: Conduct team decision voting in PRIORITY lists
    6. **Plan Events**: Create schedules and reminders

    ### Authentication

    Most APIs require JWT Token authentication. Include in header:
    ```
    Authorization: Bearer <your-jwt-token>
    ```

    ### Usage Recommendations

    * **Personal Task Management**: Use personal calendar + TODO lists
    * **Team Collaboration**: Use shared calendar + PRIORITY lists + voting system
    * **Project Management**: Mix different list types + event scheduling

    ### Related Documentation

    * [Complete API Documentation](https://github.com/your-repo/DateTree/blob/main/docs/api/rest-api.md)
    * [Workflow Examples](https://github.com/your-repo/DateTree/blob/main/docs/api/api-workflow-examples.md)
    """,
    version="1.0.0",
    contact={
        "name": "DateTree Development Team",
        "email": "support@datetree.dev",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)