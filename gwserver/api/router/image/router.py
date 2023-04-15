from gwserver.api.base.router import Base as Router
from gwserver.core import config
from gwserver.interface import image as interface

from .handler import post_image

router = Router(
    interface=interface,
    path=f"{config.API_ROOT_PATH}/image",
    tags=("Image",),
)

router.register(post_image.handler)
