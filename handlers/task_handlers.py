from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.schema_request import CreateTaskRequest, UpdateTaskRequest
from services.task_services import ITaskServices
from container.di_container import di_container
from settings.async_session import get_async_session

router_tasks = APIRouter()


@router_tasks.post("/")
async def create_task(task_request: CreateTaskRequest,
                      task_service: ITaskServices = Depends(di_container.get_task_service),
                      async_session: AsyncSession = Depends(get_async_session)):

    new_task_id = await task_service.create_task(async_session=async_session,
                                                 title=task_request.title,
                                                 description=task_request.description)

    if new_task_id is None:
        raise HTTPException(status_code=500, detail="Failed to register a new task")

    return new_task_id


@router_tasks.get("/{task_id}")
async def get_task_by_id(task_id: int,
                         task_service: ITaskServices = Depends(di_container.get_task_service),
                         async_session: AsyncSession = Depends(get_async_session)):

    task = await task_service.get_task_by_id(async_session=async_session,
                                             task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} has not been found")

    return task


@router_tasks.get("/")
async def get_all_tasks(task_service: ITaskServices = Depends(di_container.get_task_service),
                        async_session: AsyncSession = Depends(get_async_session)):

    tasks = await task_service.get_all_tasks(async_session=async_session)

    if tasks is None:
        raise HTTPException(status_code=404, detail="Tasks have not been found")

    return tasks


@router_tasks.put("/{task_id}")
async def update_task_by_id(task_id: int,
                            task_request: UpdateTaskRequest,
                            task_service: ITaskServices = Depends(di_container.get_task_service),
                            async_session: AsyncSession = Depends(get_async_session)):

    updated_task = await task_service.update_task_by_id(async_session=async_session,
                                                        title=task_request.title,
                                                        description=task_request.description,
                                                        task_id=task_id)

    if updated_task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} has not been updated")

    return updated_task


@router_tasks.delete("/{task_id}")
async def remove_task_by_id(task_id: int,
                            task_service: ITaskServices = Depends(di_container.get_task_service),
                            async_session: AsyncSession = Depends(get_async_session)):

    removed_task_id = await task_service.remove_task_by_id(async_session=async_session, task_id=task_id)

    if removed_task_id is None:
        raise HTTPException(status_code=404, detail="Not found")

    return JSONResponse(content={}, status_code=200)
