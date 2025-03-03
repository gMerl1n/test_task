import logging
from abc import ABC, abstractmethod
from domain.domain import TaskEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from repository.model import Task

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)

class ITaskRepository(ABC):

    @abstractmethod
    async def get_task_by_id(self, async_session: AsyncSession, task_id: int):
        raise NotImplemented

    @abstractmethod
    async def get_all_tasks(self, async_session: AsyncSession) -> list[TaskEntity] | None:
        raise NotImplemented

    @abstractmethod
    async def create_task(self, async_session: AsyncSession, task: TaskEntity):
        raise NotImplemented

    @abstractmethod
    async def update_task_by_id(self,
                                async_session: AsyncSession,
                                title: str,
                                description: str,
                                task_id: int) -> int | None:
        raise NotImplemented

    @abstractmethod
    async def remove_task_by_id(self, async_session: AsyncSession, task_id: int) -> int | None:
        raise NotImplemented


class TaskRepository(ITaskRepository):

    async def get_task_by_id(self, async_session: AsyncSession, task_id: int):

        query = select(Task).where(and_(Task.task_id == task_id, Task.task_id == task_id))
        task = await async_session.execute(query)
        if task is None:
            logging.warning(f"Task with id {task_id} or task id {task_id} do not exist")
            return

        task_scalar = task.scalar()
        if task_scalar is None:
            logging.warning(f"Failed to get scalar data from query task. "
                            f"Probably, task with task id {task_id} or task id {task_id} do not exist")
            return

        return TaskEntity(
            task_id=task_scalar.task_id,
            title=task_scalar.title,
            description=task_scalar.description,
            updated_at=int(task_scalar.updated_at.timestamp()),
            created_at=int(task_scalar.created_at.timestamp()),
        )

    async def get_all_tasks(self, async_session: AsyncSession) -> list[TaskEntity] | None:
        pass

    async def create_task(self, async_session: AsyncSession, task: TaskEntity):

        new_task = Task.to_task_model(task)
        async_session.add(new_task)
        await async_session.commit()
        await async_session.refresh(new_task)
        return new_task.task_id

    async def update_task_by_id(self,
                                async_session: AsyncSession,
                                title: str,
                                description: str,
                                task_id: int) -> int | None:
        pass


    async def remove_task_by_id(self, async_session: AsyncSession, task_id: int) -> int | None:
        pass