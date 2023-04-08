from .base import StaticAPIError

NotFoundByUID = StaticAPIError(
    name="NotFoundByUID",
    status_code=404,
    description="Record with the specified unique ID not found",
)
