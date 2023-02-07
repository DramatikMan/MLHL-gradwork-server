from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column

from gwserver.core.database import Base


class Image(Base):
    __tablename__ = "IMAGE"

    uid = mapped_column(Integer, primary_key=True)
