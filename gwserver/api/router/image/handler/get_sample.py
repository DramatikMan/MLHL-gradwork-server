import random
from typing import Literal

from litestar import get, status_codes
from pydantic import ConstrainedInt
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from gwserver.core.s3 import s3
from gwserver.model import Image
from gwserver.schema.error.base import StaticAPIError
from gwserver.schema.request import UID

ColorPaletteUnspecified = StaticAPIError(
    name="ColorPaletteUnspecified",
    status_code=status_codes.HTTP_400_BAD_REQUEST,
    description="Color palette unspecified when requesting specific color",
)


class Quantity(ConstrainedInt):
    ge = 1
    le = 9


@get("/sample", responses=ColorPaletteUnspecified.response)
async def handler(
    session: Session,
    qty: Quantity,
    category_uid: UID | None = None,
    color_palette: Literal["RGB", "RYB"] | None = None,
    color: str | None = None,
) -> list[str]:
    where_and_arg = [Image.uid <= 21000]

    if category_uid is not None:
        where_and_arg.append(Image.category_uid == category_uid)

    if color is not None:
        if color_palette is None:
            raise ColorPaletteUnspecified

        where_and_arg.append(getattr(Image, f"color_{color_palette.lower()}") == color)

    selected = session.execute(select(Image.uid).where(and_(*where_and_arg))).scalars().all()

    if (length := len(selected)) == 0:
        return []

    length if qty > length else int(qty)
    sampled = random.sample(selected, qty)

    return [
        s3.get_temp_link(i)
        for i in session.execute(select(Image.path).where(Image.uid.in_(sampled))).scalars()
    ]
