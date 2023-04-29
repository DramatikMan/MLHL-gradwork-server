from gwserver.api.base.router import Base as Router
from gwserver.core import config
from gwserver.interface import image as interface

from .handler import get_sample, post_image

router = Router(
    interface=interface,
    path=f"{config.API_ROOT_PATH}/image",
    tags=("Image",),
)

router.register(get_sample.handler)
router.register(post_image.handler)
