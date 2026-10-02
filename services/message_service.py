from sqlalchemy import select, func
from database.models import MessageLog, User, Group, BotStats
from database.db import async_session

async def log_message(user_id, group_id):
    async with async_session() as session:
        log = MessageLog(user_id=user_id, group_id=group_id)
        session.add(log)
        await session.commit()

async def get_bot_stats():
    async with async_session() as session:
        total_users = await session.scalar(select(func.count(User.user_id)))
        total_groups = await session.scalar(select(func.count(Group.group_id)))
        total_messages = await session.scalar(select(func.count(MessageLog.id)))
        return {
            "users": total_users or 0,
            "groups": total_groups or 0,
            "messages": total_messages or 0,
        }

async def get_top_users(limit=10):
    async with async_session() as session:
        result = await session.execute(
            select(User).order_by(User.total_messages.desc()).limit(limit)
        )
        return result.scalars().all()
