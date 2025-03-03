from sqlalchemy import Column, String, Integer, DateTime
from settings.base import Base
from datetime import datetime
from domain.domain import TaskEntity


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String(255))
    description = Column(String(1024))
    created_at = Column(DateTime, nullable=False, default=datetime.timestamp)
    updated_at = Column(DateTime, nullable=False, default=datetime.timestamp)

    @classmethod
    def to_task_model(cls, obj: TaskEntity):
        return cls(
            task_id=obj.task_id,
            title=obj.title,
            description=obj.description,
            updated_at=datetime.fromtimestamp(obj.updated_at),
            created_at=datetime.fromtimestamp(obj.created_at)
        )