from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Sequence

from gwserver import typings
from gwserver.core.database import Base

CategorySequence = Sequence("CATEGORY_uid_seq", start=1, metadata=Base.metadata)
ImageSequence = Sequence("IMAGE_uid_seq", start=1, metadata=Base.metadata)


class Category(Base):
    __tablename__ = "CATEGORY"

    uid: Mapped[int] = mapped_column(
        Integer,
        CategorySequence,
        primary_key=True,
        server_default=CategorySequence.next_value(),
    )

    title: Mapped[typings.CATEGORY] = mapped_column(String, nullable=False, unique=True)


class Image(Base):
    __tablename__ = "IMAGE"

    uid: Mapped[int] = mapped_column(
        Integer,
        ImageSequence,
        primary_key=True,
        server_default=ImageSequence.next_value(),
    )

    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    category_uid: Mapped[Optional[int]] = mapped_column(ForeignKey(Category.uid))
    category: Mapped["Category"] = relationship()
