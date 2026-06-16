from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine 
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker, mapped_column, Session


DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker[Session](bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key= True, default= lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default= False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all()
    yield


app = FastAPI(lifespan= None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods = ["*"]
)

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool 


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None= None
    completed: bool | None= None

tasks: list[TaskSchema] = []


@app.get("/tasks")
def read_tasks() -> list[TaskSchema]:
    return tasks


@app.post("/tasks", status_code= status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema)-> TaskSchema:
    new_task = TaskSchema(id= str(uuid4()), title= payload.title, completed= False)
    tasks.append(new_task)  
    return new_task


@app.patch("/tasks/{task_id}")
def create_task(task_id: str, payload: TaskUpdateSchema)-> TaskSchema:
    for task in tasks:
        if task_id == task.id:
            if payload.title:
                task.title = payload.title
            if payload.completed is not None: 
                task.completed = payload.completed
            return  task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def cdelete_task(task_id: str):
    for task in tasks:
        if task_id == task.id:
            tasks.remove(task)
            return {"message" : f"Item {task_id} has been deleted"}