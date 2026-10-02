from sqlalchemy import select, func
from database.models import User
from database.db import async_session

async def get_or_create_user(user_id, username=None, first_name=None):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(user_id=user_id, username=username, first_name=first_name)
            session.add(user)
            await session.commit()
        return user

async def increment_user_messages(user_id):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.total_messages += 1
            user.level = (user.total_messages // 100) + 1
            await session.commit()
