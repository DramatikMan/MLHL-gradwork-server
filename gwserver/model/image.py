from color_utils.constant import RGB, RYB
from color_utils.typings import COLOR_RGB, COLOR_RYB
from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Sequence

from gwserver.core.database import Base

from .category import Category

ImageSequence = Sequence("IMAGE_uid_seq", start=1, metadata=Base.metadata)


class Image(Base):
    __tablename__ = "IMAGE"

    __table_args__ = (
        CheckConstraint(f"""color_rgb IN ('{"', '".join(RGB.keys())}')""", name="RGB_check"),
        CheckConstraint(f"""color_ryb IN ('{"', '".join(RYB.keys())}')""", name="RYB_check"),
    )

    uid: Mapped[int] = mapped_column(
        Integer,
        ImageSequence,
        primary_key=True,
        server_default=ImageSequence.next_value(),
    )

    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    color_rgb: Mapped[COLOR_RGB | None] = mapped_column(String)
    color_ryb: Mapped[COLOR_RYB | None] = mapped_column(String)

    category_uid: Mapped[int | None] = mapped_column(
        ForeignKey(
            Category.uid,
            name="category_uid_fk",
        )
    )

    category: Mapped["Category"] = relationship()
