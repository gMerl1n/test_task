from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from domain.domain import TaskEntity
from pytz import timezone as tz
from datetime import datetime
from repository.task_repository import ITaskRepository


class ITaskServices(ABC):

    @abstractmethod
    async def get_task_by_id(self, async_session: AsyncSession, task_id: int) -> int | None:
        raise NotImplemented

    @abstractmethod
    async def get_all_tasks(self, async_session: AsyncSession) -> list[TaskEntity] | None:
        raise NotImplemented

    @abstractmethod
    async def create_task(self, async_session: AsyncSession, title: str, description: str) -> int:
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


class TaskService(ITaskServices):

    def __init__(self, task_repo: ITaskRepository):
        self.__task_repo = task_repo

    async def get_task_by_id(self, async_session: AsyncSession, task_id: int) -> TaskEntity | None:
        task = await self.__task_repo.get_task_by_id(async_session=async_session,
                                                                 task_id=task_id)
        return task

    async def get_all_tasks(self, async_session: AsyncSession) -> list[TaskEntity] | None:
        tasks = await self.__task_repo.get_all_tasks(async_session=async_session)
        return tasks

    async def create_task(self, async_session: AsyncSession, title: str, description: str) -> int:

        moscow_tz = tz('Europe/Moscow')

        new_task = TaskEntity(
            title=title,
            description=description,
            updated_at=int(datetime.now(moscow_tz).timestamp()),
            created_at=int(datetime.now(moscow_tz).timestamp()),
        )

        new_task_id = await self.__task_repo.create_task(async_session=async_session,
                                                         task=new_task)
        return new_task_id

    async def update_task_by_id(self,
                                async_session: AsyncSession,
                                title: str,
                                description: str,
                                task_id: int) -> int | None:

        pass

    async def remove_task_by_id(self, async_session: AsyncSession, task_id: int) -> int | None:

        removed_task_id = await self.__task_repo.remove_task_by_id(async_session=async_session,
                                                                   task_id=task_id)
        return removed_task_id
