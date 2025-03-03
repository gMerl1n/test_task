from fastapi import APIRouter
from handlers.task_handlers import router_tasks

routes = APIRouter()

routes.include_router(router=router_tasks, prefix="/tasks")
