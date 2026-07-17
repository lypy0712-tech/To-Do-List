from fastapi import Depends, HTTPException, status, APIRouter

from app.api.dependencies import get_task_services
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from app.services.task import TaskNotFound, TaskServices


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("")
def read_tasks(task_service: TaskServices = Depends(get_task_services)) -> list[TaskSchema]:
    return task_service.list_task()

@router.post("", status_code= status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, 
                task_service: TaskServices = Depends(get_task_services)) -> TaskSchema:
    return task_service.create_task(task_create=payload)

@router.patch("/{task_id}", status_code= status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdateSchema, 
                task_service: TaskServices = Depends(get_task_services))-> TaskSchema:
                try:
                    return task_service.task_update(task_id, task_update= payload)
                except TaskNotFound:
                      HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskServices = Depends(get_task_services)) -> None:
    try:
        return task_service.task_delete(task_id)
    except TaskNotFound:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND)
