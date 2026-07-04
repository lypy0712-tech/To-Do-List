from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, Session, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://postgres:admin@192.168.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal= sessionmaker[Session](bind=engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    id: Mapped[str]= mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__= "tasks"

    title: Mapped[str]
    completed: Mapped[bool]= mapped_column(default=False)


@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title= "To-Do-List"
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods = ["*"]
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool 

    model_config={
        "from_attributes":True
    }


class TaskCreateSchema(BaseModel):
    title: str

    model_config={
        "from_attributes":True
    }


class TaskUpdateSchema(BaseModel):
    title: str | None= None
    completed: bool | None= None

    model_config={
        "from_attributes":True
    }

def task_orm_to_model(task_orm: TaskORM):
    return TaskSchema(id= task_orm.id, title= task_orm.title, completed=task_orm.completed)


@app.get("/tasks")
def read_tasks(db: Session= Depends(get_db), response_model= TaskSchema) -> list[TaskSchema]:
    task_from_db= db.scalars(select(TaskORM)).all()
    return task_from_db


@app.post("/tasks", status_code= status.HTTP_200_OK)
def create_task(payload: TaskCreateSchema, db: Session= Depends(get_db)) -> TaskSchema:
    new_task = TaskORM(title= payload.title, completed= False)
    db.add(new_task) 
    db.commit()
    return new_task


@app.patch("/tasks/{task_id}", status_code= status.HTTP_200_OK)
def create_task(task_id: str, payload: TaskUpdateSchema, db: Session= Depends(get_db), response_model= TaskSchema)-> TaskSchema:
    response = db.get(TaskORM, task_id)
    if response:
        if payload.title:
            response.title = payload.title
        if payload.completed is not None:
            response.completed = payload.completed
        db.commit()
        return response
    return HTTPException(status_code= 404, detail= f"Task with {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session= Depends(get_db)) -> None:
    task_for_delete= db.get(TaskORM, task_id)
    db.delete(task_for_delete)
    db.commit()