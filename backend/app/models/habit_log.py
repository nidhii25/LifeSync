from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey,
    Date,
    DateTime
)

from datetime import (
    date,
    datetime
)

from app.database.database import Base


class HabitLog(Base):

    __tablename__ = "habit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    habit_id = Column(
        Integer,
        ForeignKey("habits.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    date = Column(
        Date,
        default=date.today
    )

    completed = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )