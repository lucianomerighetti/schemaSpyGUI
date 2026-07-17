from enum import StrEnum

class EventType(StrEnum):
    CONNECTION_CREATED = "connection.created"
    CONNECTION_UPDATED = "connection.updated"
    CONNECTION_DELETED = "connection.deleted"
    CONNECTION_SELECTED = "connection.selected"
    CONNECTION_TESTED = "connection.tested"
    VALIDATION_FAILED = "validation.failed"
    VALIDATION_SUCCESS = "validation.success"