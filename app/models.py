from typing import Optional
from datetime import datetime, timezone
from app import db, login
from sqlalchemy import orm
import sqlalchemy as sa
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from uuid import UUID


@login.user_loader
def load_user(user_id: str) -> Optional['User']:
    return db.session.get(User, UUID(user_id))


class User(UserMixin, db.Model):
    id: orm.Mapped[sa.Uuid] = orm.mapped_column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    username: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(120), unique=True, index=True)
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(256))
    posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates="author")

    def __repr__(self) -> str:
        return f'<User: {self.username}, Email: {self.email}, ID: {self.id}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id: orm.Mapped[sa.Uuid] = orm.mapped_column(sa.Uuid, primary_key=True, default=uuid.uuid4)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(140))
    body: orm.Mapped[str] = orm.mapped_column(sa.String(500))
    user_id: orm.Mapped[sa.Uuid] = orm.mapped_column(sa.ForeignKey(User.id))
    timestamp: orm.Mapped[datetime] = orm.mapped_column(default=lambda: datetime.now(timezone.utc), index=True)
    author: orm.Mapped[User] = orm.relationship(back_populates="posts")

    def __repr__(self):
        return f'<Post: {self.title} by User ID: {self.user_id}>'
