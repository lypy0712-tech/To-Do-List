from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task import TaskServices
from app.services.category import CategoryServices

def get_task_services(db: Session = Depends(get_db)):
    return TaskServices(db)

def get_category_service(db: Session= Depends(get_db)):
    return CategoryServices(db)