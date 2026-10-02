from sqlalchemy import select, func, desc
from datetime import datetime, timedelta
import logging

from database.models import MessageLog, User, Group, GroupMilestone
from database.db import async_session

logger = logging.getLogger(__name__)

IST_OFFSET = timedelta(hours=5, minutes=30)


def _ist_now():
    return datetime.utcnow() + IST_OFFSET


def _today_ist_str():
    return _ist_now().strftime("%Y-%m-%d")


def _midnight_ist_utc():
    now_ist = _ist_now()
    midnight_ist = now_ist.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight_ist - IST_OFFSET


def _group_link(group_id: int) -> str:
    """
    Private supergroup link banata hai.
    Format: https://t.me/c/{id_without_-100}/1
    """
    gid_str = str(group_id)
    if gid_str.startswith("-100"):
        bare = gid_str[4:]
        return f"https://t.me/c/{bare}/1"
    # Fallback for normal groups
    return f"https://t.me/c/{gid_str.lstrip('-')}/1"


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
    now = datetime.utcnow()
    cutoff = None
    if timeframe == "today":
        cutoff = _midnight_ist_utc()
    elif timeframe == "weekly":
        cutoff = now - timedelta(days=7)
    elif timeframe == "monthly":
        cutoff = now - timedelta(days=30)

    async with async_session() as session:
        query = select(
            MessageLog.user_id,
            func.count(MessageLog.id).label("msg_count"),
        ).where(MessageLog.group_id == group_id)

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

        out = []
        for uid, count in rows:
            u = users_map.get(uid)
            name = "ᴜsᴇʀ"
            if u:
                name = u.first_name or u.username or f"ᴜsᴇʀ {uid}"
            out.append({"user_id": uid, "name": name, "messages": count})
        return out


async def get_user_groups_with_counts(user_id, timeframe="all", limit=20):
    """
    Returns list of dicts:
      {group_id, title, link, count}
    """
    now = datetime.utcnow()
    cutoff = None
    if timeframe == "today":
        cutoff = _midnight_ist_utc()
    elif timeframe == "weekly":
        cutoff = now - timedelta(days=7)
    elif timeframe == "monthly":
        cutoff = now - timedelta(days=30)

    async with async_session() as session:
        query = select(
            MessageLog.group_id,
            func.count(MessageLog.id).label("cnt"),
        ).where(MessageLog.user_id == user_id)

        if cutoff:
            query = query.where(MessageLog.timestamp >= cutoff)

        query = (
            query.group_by(MessageLog.group_id)
            .order_by(desc("cnt"))
            .limit(limit)
        )

        result = await session.execute(query)
        rows = result.all()
        if not rows:
            return []

        group_ids = [r[0] for r in rows]
        groups_result = await session.execute(
            select(Group).where(Group.group_id.in_(group_ids))
        )
        groups_map = {g.group_id: g for g in groups_result.scalars().all()}

        out = []
        for gid, cnt in rows:
            g = groups_map.get(gid)
            title = (g.title if g and g.title else f"ɢʀᴏᴜᴘ {gid}")
            out.append({
                "group_id": gid,
                "title": title,
                "link": _group_link(gid),
                "count": cnt,
            })
        return out


# ─────────────────────────────────────────────────────────
#  MILESTONE
# ─────────────────────────────────────────────────────────

def get_milestone_thresholds():
    thresholds = {300, 500}
    n = 1000
    while n <= 10_000_000:
        thresholds.add(n)
        n += 500
    return thresholds


async def get_today_message_count(group_id):
    cutoff = _midnight_ist_utc()
    async with async_session() as session:
        count = await session.scalar(
            select(func.count(MessageLog.id)).where(
                MessageLog.group_id == group_id,
                MessageLog.timestamp >= cutoff,
            )
        )
        return count or 0


async def maybe_send_milestone(bot, group_id, count):
    if count not in get_milestone_thresholds():
        return

    today_str = _today_ist_str()

    async with async_session() as session:
        existing = await session.scalar(
            select(func.count(GroupMilestone.id)).where(
                GroupMilestone.group_id == group_id,
                GroupMilestone.milestone == count,
                GroupMilestone.date == today_str,
            )
        )
        if existing and existing > 0:
            return

        session.add(GroupMilestone(
            group_id=group_id,
            milestone=count,
            date=today_str,
        ))
        await session.commit()

    ist_time = _ist_now().strftime("%H:%M")
    next_target = count + (500 if count >= 1000 else (200 if count == 300 else 500))

    text = (
        f"🏆 <b>{count} ᴍᴇssᴀɢᴇs ʀᴇᴀᴄʜᴇᴅ ᴛᴏᴅᴀʏ!</b>\n"
        f"⏰ ᴛɪᴍᴇ: <b>{ist_time}</b>\n\n"
        f"🔥 ᴀᴡᴇsᴏᴍᴇ! ᴋᴇᴇᴘ ᴛʜᴇ ᴄʜᴀᴛ ᴀʟɪᴠᴇ!\n"
        f"🎯 ɴᴇxᴛ ᴍɪʟᴇsᴛᴏɴᴇ: <b>{next_target}</b> ᴍsɢs"
    )

    try:
        await bot.send_message(
            chat_id=group_id,
            text=text,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.error(f"Milestone send failed for {group_id}: {e}")
