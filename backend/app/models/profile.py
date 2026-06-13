from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)

from datetime import datetime

from app.database.database import Base


class Profile(Base):

    __tablename__ = "profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    age = Column(Integer)

    gender = Column(String)

    height_cm = Column(Float)

    current_weight = Column(Float)

    target_weight = Column(Float)

    occupation = Column(String)

    bio = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )