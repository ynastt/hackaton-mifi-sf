import uuid
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Exhibit(Base):
    __tablename__ = 'exhibits'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    label: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, onupdate=func.now())


    comments: Mapped[List['Comment']] = relationship('Comment',
                                                     cascade='all, delete, delete-orphan',
                                                     back_populates='exhibit',
                                                     lazy='selectin'
                                                     )


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    exhibit_id: Mapped[UUID] = mapped_column(ForeignKey('exhibits.id', ondelete='CASCADE'), nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    sentiment: Mapped[int] = mapped_column(nullable=True)
    exhibit: Mapped[Exhibit] = relationship(back_populates='comments', lazy='selectin')
    created_at: Mapped[datetime] = mapped_column(nullable=True, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, onupdate=func.now())
