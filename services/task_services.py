import logging
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from domain.domain import TaskEntity
from datetime import datetime
from repository.task_repository import ITaskRepository
from settings.exceptions import InvalidTaskTitleField
from settings.settings import config


class ITaskServices(ABC):

    @abstractmethod
    async def get_task_by_id(self, async_session: AsyncSession, task_id: int) -> TaskEntity | None:
        raise NotImplemented

    @abstractmethod
    async def get_all_tasks(self, async_session: AsyncSession) -> list[TaskEntity] | None:
        raise NotImplemented

    @abstractmethod
    async def create_task(self, async_session: AsyncSession, title: str, description: str) -> int | None:
        raise NotImplemented

    @abstractmethod
    async def update_task_by_id(self,
                                async_session: AsyncSession,
                                title: str,
                                description: str,
                                task_id: int) -> TaskEntity | None:
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

    async def create_task(self, async_session: AsyncSession, title: str, description: str) -> int | None:

        try:
            new_task = TaskEntity(
                title=title,
                description=description,
                updated_at=int(datetime.now(config.moscow_tz).timestamp()),
                created_at=int(datetime.now(config.moscow_tz).timestamp()),
            )

        except InvalidTaskTitleField as ex:
            logging.warning(f"Failed to create a new task. Invalid title field: {ex}")
            return

        else:
            new_task_id = await self.__task_repo.create_task(async_session=async_session,
                                                             task=new_task)
            return new_task_id

    async def update_task_by_id(self,
                                async_session: AsyncSession,
                                title: str,
                                description: str,
                                task_id: int) -> TaskEntity | None:

        time_updated = int(datetime.now(config.moscow_tz).timestamp())

        updated_task_id = await self.__task_repo.update_task_by_id(async_session=async_session,
                                                                   title=title,
                                                                   description=description,
                                                                   time_updated=time_updated,
                                                                   task_id=task_id)

        if updated_task_id is None:
            return

        task = await self.__task_repo.get_task_by_id(async_session=async_session,
                                                     task_id=task_id)
        return task

    async def remove_task_by_id(self, async_session: AsyncSession, task_id: int) -> int | None:

        removed_task_id = await self.__task_repo.remove_task_by_id(async_session=async_session,
                                                                   task_id=task_id)
        return removed_task_id
