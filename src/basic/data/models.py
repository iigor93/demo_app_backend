from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func, text
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base
from src.storage import banner_storage


class Banner(Base):
    __tablename__ = "banners"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    image: Mapped[str] = mapped_column(
        FileType(storage=banner_storage),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
