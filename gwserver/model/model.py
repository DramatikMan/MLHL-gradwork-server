from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from gwserver.core.database import Base


class Category(Base):
    __tablename__ = "CATEGORY"

    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class Image(Base):
    __tablename__ = "IMAGE"

    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    category_uid: Mapped[int] = mapped_column(ForeignKey(Category.uid), nullable=False)
