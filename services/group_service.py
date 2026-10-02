from sqlalchemy import select, func
from database.models import Group, GroupMember
from database.db import async_session

async def get_or_create_group(group_id, title=None, added_by=None):
    async with async_session() as session:
        result = await session.execute(select(Group).where(Group.group_id == group_id))
        group = result.scalar_one_or_none()
        if not group:
            group = Group(group_id=group_id, title=title, added_by=added_by)
            session.add(group)
            await session.commit()
        return group

async def increment_group_messages(group_id):
    async with async_session() as session:
        result = await session.execute(select(Group).where(Group.group_id == group_id))
        group = result.scalar_one_or_none()
        if group:
            group.total_messages += 1
            await session.commit()

async def update_group_member(group_id, user_id):
    async with async_session() as session:
        result = await session.execute(
            select(GroupMember).where(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            )
        )
        member = result.scalar_one_or_none()
        if member:
            member.messages_in_group += 1
        else:
            member = GroupMember(group_id=group_id, user_id=user_id, messages_in_group=1)
            session.add(member)
        await session.commit()
