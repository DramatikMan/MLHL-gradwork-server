from litestar import post

from gwserver.api.base.router import Base as Router
from gwserver.core import config
from gwserver.interface import image as interface

from .handler import post_image

router = Router(
    interface=interface,
    path=f"{config.API_ROOT_PATH}/image",
    tags=("Image",),
)

router.register(
    post(
        content_media_type="image/jpeg",
        responses=post_image.ImageOpenFailure.response | post_image.ImageNotSquare.response,
    )(post_image.handler)
)
