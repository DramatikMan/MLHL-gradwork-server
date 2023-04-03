from typing import Optional

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Sequence

import color_utils.typings as color
from gwserver.core.database import Base

from .category import Category
from .constant import RGBt, RYBt

ImageSequence = Sequence("IMAGE_uid_seq", start=1, metadata=Base.metadata)


class Image(Base):
    __tablename__ = "IMAGE"

    __table_args__ = (
        CheckConstraint(f"""color_rgb in ('{"', '".join(RGBt.keys())}')"""),
        CheckConstraint(f"""color_ryb in ('{"', '".join(RYBt.keys())}')"""),
    )

    uid: Mapped[int] = mapped_column(
        Integer,
        ImageSequence,
        primary_key=True,
        server_default=ImageSequence.next_value(),
    )

    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    category_uid: Mapped[Optional[int]] = mapped_column(ForeignKey(Category.uid))
    category: Mapped["Category"] = relationship(lazy=False)

    color_rgb: Mapped[Optional[color.COLOR_RGB]] = mapped_column(String)
    color_ryb: Mapped[Optional[color.COLOR_RYB]] = mapped_column(String)
