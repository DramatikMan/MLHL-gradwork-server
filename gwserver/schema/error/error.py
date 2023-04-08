from litestar import status_codes

from .base import StaticAPIError

NotFoundByUID = StaticAPIError(
    name="NotFoundByUID",
    status_code=status_codes.HTTP_404_NOT_FOUND,
    description="Record with the specified unique ID not found",
)
