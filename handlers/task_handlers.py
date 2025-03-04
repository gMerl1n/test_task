from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
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
                      async_session: AsyncSession = Depends(get_async_session)) -> JSONResponse:

    new_task_id = await task_service.create_task(async_session=async_session,
                                                 title=task_request.title,
                                                 description=task_request.description)

    if new_task_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register a new task")

    return JSONResponse(content={"new_task_id": new_task_id}, status_code=status.HTTP_201_CREATED)


@router_tasks.get("/{task_id}")
async def get_task_by_id(task_id: int,
                         task_service: ITaskServices = Depends(di_container.get_task_service),
                         async_session: AsyncSession = Depends(get_async_session)) -> JSONResponse:

    task = await task_service.get_task_by_id(async_session=async_session,
                                             task_id=task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} has not been found")

    return JSONResponse(content=task.to_dict(), status_code=status.HTTP_201_CREATED)


@router_tasks.get("/")
async def get_all_tasks(task_service: ITaskServices = Depends(di_container.get_task_service),
                        async_session: AsyncSession = Depends(get_async_session)) -> JSONResponse:

    tasks = await task_service.get_all_tasks(async_session=async_session)

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks have not been found")

    return JSONResponse(content=[t.to_dict() for t in tasks], status_code=status.HTTP_200_OK)


@router_tasks.put("/{task_id}")
async def update_task_by_id(task_id: int,
                            task_request: UpdateTaskRequest,
                            task_service: ITaskServices = Depends(di_container.get_task_service),
                            async_session: AsyncSession = Depends(get_async_session)) -> JSONResponse:

    updated_task = await task_service.update_task_by_id(async_session=async_session,
                                                        title=task_request.title,
                                                        description=task_request.description,
                                                        task_id=task_id)

    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {task_id} has not been updated")

    return JSONResponse(content=updated_task.to_dict(), status_code=status.HTTP_200_OK)


@router_tasks.delete("/{task_id}")
async def remove_task_by_id(task_id: int,
                            task_service: ITaskServices = Depends(di_container.get_task_service),
                            async_session: AsyncSession = Depends(get_async_session)) -> JSONResponse:

    removed_task_id = await task_service.remove_task_by_id(async_session=async_session, task_id=task_id)

    if removed_task_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return JSONResponse(content={}, status_code=200)
