from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
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

class BotStats(Base):
    __tablename__ = "bot_stats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_users = Column(Integer, default=0)
    total_groups = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    daily_active = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
