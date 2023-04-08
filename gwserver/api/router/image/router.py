from litestar import post

from gwserver.api.base.router import Base as Router
from gwserver.core import config
from gwserver.interface import image as interface

from . import handler

router = Router(
    interface=interface,
    path=f"{config.API_ROOT_PATH}/image",
    tags=("Image",),
)

router.register(post(content_media_type="image/jpeg")(handler.post_image))
