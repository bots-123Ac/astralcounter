from sqlalchemy import select, func, desc
from datetime import datetime, timedelta
from database.models import MessageLog, User, Group, GroupMember
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


async def get_group_top_users(group_id, limit=10, timeframe="all"):
    """
    timeframe: all | monthly | weekly | today
    Returns list of dicts: {user_id, name, messages}
    """
    now = datetime.utcnow()
    cutoff = None
    if timeframe == "today":
        cutoff = now - timedelta(hours=24)
    elif timeframe == "weekly":
        cutoff = now - timedelta(days=7)
    elif timeframe == "monthly":
        cutoff = now - timedelta(days=30)

    async with async_session() as session:
        query = (
            select(
                MessageLog.user_id,
                func.count(MessageLog.id).label("msg_count"),
            )
            .where(MessageLog.group_id == group_id)
        )
        if cutoff:
            query = query.where(MessageLog.timestamp >= cutoff)

        query = (
            query.group_by(MessageLog.user_id)
            .order_by(desc("msg_count"))
            .limit(limit)
        )

        result = await session.execute(query)
        rows = result.all()

        if not rows:
            return []

        user_ids = [r[0] for r in rows]
        users_result = await session.execute(
            select(User).where(User.user_id.in_(user_ids))
        )
        users_map = {u.user_id: u for u in users_result.scalars().all()}

        top = []
        for uid, count in rows:
            u = users_map.get(uid)
            name = "ᴜsᴇʀ"
            if u:
                name = u.first_name or u.username or f"ᴜsᴇʀ {uid}"
            top.append({
                "user_id": uid,
                "name": name,
                "messages": count,
            })
        return top
