from .base import StaticAPIError

NOT_FOUND_BY_UID = StaticAPIError(
    name="NOT_FOUND_BY_UID",
    status_code=404,
    description="Record with the specified unique ID not found",
)
