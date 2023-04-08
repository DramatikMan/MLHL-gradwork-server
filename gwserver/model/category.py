from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import Sequence

from gwserver.core.database import Base

CategorySequence = Sequence("CATEGORY_uid_seq", start=1, metadata=Base.metadata)


class Category(Base):
    __tablename__ = "CATEGORY"

    uid: Mapped[int] = mapped_column(
        Integer,
        CategorySequence,
        primary_key=True,
        server_default=CategorySequence.next_value(),
    )

    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
