import punq
from repository.task_repository import ITaskRepository, TaskRepository
from services.task_services import ITaskServices, TaskService


class DIContainer:

    container = punq.Container()

    container.register(ITaskRepository, TaskRepository)
    container.register(ITaskServices, TaskService)

    def get_task_service(self) -> ITaskServices:
        return self.container.resolve(ITaskServices)


di_container = DIContainer()
