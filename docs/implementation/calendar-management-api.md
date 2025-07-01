# Calendar Management API

This document details the API endpoints for managing calendars. Calendars act as containers for lists and events.

## Key Concepts

*   **Calendar Types**: There are two types of calendars:
    *   `PERSONAL`: An auto-created, non-deletable calendar for each user.
    *   `GENERAL`: Standard calendars created by users, which can be deleted.
*   **Authentication**: All endpoints require a valid JWT Bearer Token in the `Authorization` header.

## Endpoints

### 1. Create a Calendar

Creates a new `GENERAL` type calendar.

*   **Endpoint**: `POST /api/v1/calendars/`
*   **Success Response**: `200 OK`
*   **Body**:
    ```json
    {
      "name": "My New Calendar",
      "description": "Optional description for the calendar."
    }
    ```
*   **Response Body**:
    ```json
    {
      "id": 2,
      "name": "My New Calendar",
      "description": "Optional description for the calendar.",
      "owner_id": 1,
      "calendar_type": "GENERAL",
      "created_at": "2025-06-30T12:00:00.000Z",
      "owner": { ... },
      "members": [ ... ]
    }
    ```

### 2. Get All Calendars for a User

Retrieves a list of all calendars (both `PERSONAL` and `GENERAL`) owned by the authenticated user.

*   **Endpoint**: `GET /api/v1/calendars/`
*   **Success Response**: `200 OK`
*   **Response Body**: A JSON array of calendar objects.

### 3. Get a Specific Calendar

Retrieves a single calendar by its ID.

*   **Endpoint**: `GET /api/v1/calendars/{calendar_id}`
*   **Success Response**: `200 OK`
*   **Error Responses**:
    *   `404 Not Found`: If the calendar does not exist.
    *   `403 Forbidden`: If the user is not the owner of the calendar.

### 4. Update a Calendar

Updates the details of a specific calendar.

*   **Endpoint**: `PUT /api/v1/calendars/{calendar_id}`
*   **Success Response**: `200 OK`
*   **Body**:
    ```json
    {
      "name": "Updated Calendar Name",
      "description": "Updated description."
    }
    ```

### 5. Delete a Calendar

Deletes a calendar. **Note: `PERSONAL` calendars cannot be deleted.**

*   **Endpoint**: `DELETE /api/v1/calendars/{calendar_id}`
*   **Success Response**: `200 OK`
*   **Error Responses**:
    *   `404 Not Found`: If the calendar does not exist.
    *   `403 Forbidden`: If the user is not the owner or if the calendar is of type `PERSONAL`.
