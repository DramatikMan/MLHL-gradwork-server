import random

from litestar import get
from pydantic import ConstrainedInt
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from gwserver.core.s3 import s3
from gwserver.model import Image
from gwserver.schema.request import UID


class Quantity(ConstrainedInt):
    ge = 1
    le = 9


@get("/sample")
async def handler(
    session: Session,
    category_uid: UID | None,
    qty: Quantity,
) -> list[str]:
    where_and_arg = [Image.uid <= 21000]

    if category_uid is not None:
        where_and_arg.append(Image.category_uid == category_uid)

    selected_UIDs = random.sample(
        session.execute(select(Image.uid).where(and_(*where_and_arg))).scalars().all(),
        qty,
    )

    return [
        s3.get_temp_link(i)
        for i in session.execute(select(Image.path).where(Image.uid.in_(selected_UIDs))).scalars()
    ]
