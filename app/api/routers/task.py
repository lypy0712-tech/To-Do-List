from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.task import TaskService
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.api.dependencies import get_task_service

router = APIRouter(prefix="/tasks")

@router.get("")
def read_tasks(task_service: TaskService= Depends(get_task_service), response_model= TaskSchema) -> list[TaskSchema]:
    return task_service.list_tasks()

@router.get("/{task_id}", status_code= status.HTTP_200_OK)
def read_task_by_id(task_id:str, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return task_service.get_by_id(task_id)


@router.post("", status_code= status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, task_service: TaskService= Depends(get_task_service)) -> TaskSchema:
   return task_service.create_task(task_create=payload)

@router.patch("/{task_id}", status_code= status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdateSchema, db: Session= Depends(get_task_service), response_model= TaskSchema)-> TaskSchema:
  ...


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session= Depends(get_task_service)) -> None:
    ...