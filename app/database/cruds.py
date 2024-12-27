from datetime import timedelta
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import *


class DatabaseCRUDS:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_comment(self, comment: str, exhibit_id: UUID) -> Comment:
        comment = Comment(comment=comment, exhibit_id=exhibit_id)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment

    async def update_comment_sentiment(self, comment_id: UUID, sentiment: int):
        comment = await self.session.get(Comment, comment_id)
        comment.sentiment = sentiment
        await self.session.commit()
        await self.session.refresh(comment)
        return comment