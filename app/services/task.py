from sqlalchemy.orm import Session
from app.repositories.task import TaskRepository
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema

class TaskNotFound(Exception):
       """if task with entered ID is not"""

class TaskServices:
    def __init__(self, db:Session) -> None:
        self.db = db
        self.task_repository= TaskRepository(db)

    
    def list_task(self) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
         task_orm = self.task_repository.create(task_create)
         self.db.commit()
         return TaskSchema.model_validate(task_orm)
    

    def task_update(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = self.task_repository.get_by_id(task_id)
        if task_for_update is None:
            raise TaskNotFound(f"Task with {task_id} not found")
        
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        self.db.commit()
        return task_for_update

    def task_delete(self, task_id: str) -> None:
        task_for_delete = self.task_repository.get_by_id(task_id)
        if task_for_delete is None:
            raise TaskNotFound(f"Task with {task_id} not found")
        self.db.delete(task_for_delete)
        self.db.commit()


