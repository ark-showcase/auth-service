from typing import Any, List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Requests(Base):
    __tablename__ = 'requests'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='requests_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    client_ip: Mapped[Any] = mapped_column(INET)
    http_method: Mapped[str] = mapped_column(String(10))
    request_path: Mapped[str] = mapped_column(Text)
    query_string: Mapped[str] = mapped_column(Text)
    user_agent: Mapped[str] = mapped_column(Text)
    referrer: Mapped[str] = mapped_column(Text)
    content_type: Mapped[str] = mapped_column(String(255))
    headers: Mapped[Optional[dict]] = mapped_column(JSONB)
    cookies: Mapped[Optional[dict]] = mapped_column(JSONB)
    session_id: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    response_status: Mapped[Optional[int]] = mapped_column(Integer)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer)


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='roles_pkey'),
        UniqueConstraint('name', name='roles_name_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    user: Mapped[List['Users']] = relationship('Users', secondary='user_roles', back_populates='role')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('username', name='users_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(Text)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    role: Mapped[List['Roles']] = relationship('Roles', secondary='user_roles', back_populates='user')
    tokens: Mapped[List['Tokens']] = relationship('Tokens', back_populates='user')


class Tokens(Base):
    __tablename__ = 'tokens'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='tokens_user_id_fkey'),
        PrimaryKeyConstraint('id', name='tokens_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    refresh_token: Mapped[str] = mapped_column(Text)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    user: Mapped['Users'] = relationship('Users', back_populates='tokens')


t_user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('role_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='user_roles_role_id_fkey'),
    ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_roles_user_id_fkey'),
    PrimaryKeyConstraint('user_id', 'role_id', name='user_roles_pkey')
)
