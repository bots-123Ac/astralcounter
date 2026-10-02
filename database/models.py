from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Index
from datetime import datetime
from database.db import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    total_messages = Column(Integer, default=0)
    level = Column(Integer, default=1)
    gifts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Group(Base):
    __tablename__ = "groups"
    group_id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=True)
    added_by = Column(BigInteger, nullable=True)
    total_messages = Column(Integer, default=0)
    members_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class GroupMember(Base):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    messages_in_group = Column(Integer, default=0)


class MessageLog(Base):
    __tablename__ = "message_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    group_id = Column(BigInteger, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_msglog_group_time", "group_id", "timestamp"),
        Index("ix_msglog_user_group_time", "user_id", "group_id", "timestamp"),
    )


class GroupMilestone(Base):
    __tablename__ = "group_milestones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, nullable=False)
    milestone = Column(Integer, nullable=False)
    date = Column(String, nullable=False)   # YYYY-MM-DD (IST)
    created_at = Column(DateTime, default=datetime.utcnow)
