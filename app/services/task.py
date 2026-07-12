
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.repositories.task import TaskRepository

class TaskService():
    def __init__(self, db) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)


    def list_tasks(self) -> list[TaskSchema]:
        task_orm = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in task_orm]
    
    def get_by_id(self, task_id:str) -> TaskSchema:
        task_orm = self.task_repository.get_by_id(task_id)
        return TaskSchema.model_validate(task_orm)
    
    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repository.create(title= task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)