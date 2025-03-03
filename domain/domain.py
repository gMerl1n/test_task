from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TaskEntity:
    title: str
    description: str
    updated_at: int
    created_at: int
    task_id: Optional[int] = field(default=None)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def to_model(cls, dict_obj):
        return cls(**dict_obj)