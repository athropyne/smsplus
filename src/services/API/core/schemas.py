import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String, unique=True, nullable=False),
    Column("password", String, nullable=False)
)

messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sender", ForeignKey(users.c.id, onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False),
    Column("receiver", ForeignKey(users.c.id, onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", DateTime, nullable=False)
)

tg = Table(
    "telegram IDs",
    metadata,
    Column("id", ForeignKey(users.c.id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("tg_id", Integer, nullable=False)
)