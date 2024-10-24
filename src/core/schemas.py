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
    Column("from", ForeignKey(users.c.id, onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False),
    Column("to", ForeignKey(users.c.id, onupdate="NO ACTION", ondelete="NO ACTION"), nullable=False),
    Column("text", String, nullable=False),
    Column("created_at", DateTime, nullable=False, default=datetime.datetime.now())
)