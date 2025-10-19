from typing import Optional
from datetime import datetime, timezone
from app import db
from sqlalchemy import orm
import sqlalchemy as sa
import uuid

class User(db.Model):
    id: orm.Mapped[sa.Uuid] = orm.mapped_column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    # id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(120), unique=True, index=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(256))
    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates="author")

    def __repr__(self) -> str:
        return f'<User: {self.username}, Email: {self.email}, ID: {self.id}>'

class Post(db.Model):
    id: orm.Mapped[sa.Uuid] = orm.mapped_column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(140))
    body: orm.Mapped[str] = orm.mapped_column(sa.String(500))
    user_id: orm.Mapped[sa.Uuid] = orm.mapped_column(sa.ForeignKey(User.id))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(default=lambda: datetime.now(timezone.utc), index=True)
    author: orm.Mapped[User] = orm.relationship(back_populates="posts")

    def __repr__(self):
        return f'<Post: {self.title} by User ID: {self.user_id}>'