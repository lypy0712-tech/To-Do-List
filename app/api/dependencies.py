from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.task import TaskServices

def get_task_services(db: Session = Depends(get_db)):
    return TaskServices(db)