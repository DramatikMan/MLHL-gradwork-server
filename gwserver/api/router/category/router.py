from gwserver.api.base.router import Listable as Router
from gwserver.core import config
from gwserver.interface import category as interface

router = Router(
    interface=interface,
    path=f"{config.API_ROOT_PATH}/category",
    tags=("Category",),
)
