from pydantic import BaseModel


class CreateTaskRequest(BaseModel):
    title: str
    description: str


class UpdateTaskRequest(BaseModel):
    title: str
    description: str
