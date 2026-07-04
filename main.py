from uuid import uuid4
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, Mapped, mapped_column

DATABASE_URL = "postgresql+psycopg://postgres:admin@81.17.83.242:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker[Session](bind=engine)

def get_db():
    db= Sessionlocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    id: Mapped[str]= mapped_column(primary_key=True, default= lambda: str(uuid4()))


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool]= mapped_column(default=False)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

    model_config = {
        "from_attributes": True
    }


class TaskCreateSchema(BaseModel):
    title: str

    model_config = {
        "from_attributes": True
    }

class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None
    
    model_config = {
        "from_attributes": True
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def task_orm_to_model(task_orm:TaskORM) -> TaskSchema:
    return TaskSchema(id= task_orm.id, title= task_orm.title, completed= task_orm.completed)


app = FastAPI(
    title= "My To-Do-List",
    lifespan=lifespan
)

origins = [
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:3000"],
    allow_methods= ["*"],
    allow_headers=['*']
)

tasks: TaskSchema = []


@app.get("/tasks", status_code=status.HTTP_200_OK, response_model=list[TaskSchema])
def read_task(db: Session= Depends(get_db)) -> list[TaskSchema]:
    task_from_db= db.scalars(select(TaskORM)).all()
    return task_from_db


@app.post("/tasks", response_model= TaskSchema, status_code=status.HTTP_201_CREATED)
def task_create(payload: TaskCreateSchema, db: Session= Depends(get_db)) -> TaskSchema:
    new_task= TaskORM(title= payload.title, completed= False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model= TaskSchema, status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdateSchema, db= Depends(get_db)) -> TaskSchema:
    task_from_db = db.get(TaskORM, task_id)
    if payload.title:
        task_from_db.title= payload.title
    if payload.completed:
        task_from_db.completed= payload.completed
    else:
        task_from_db.completed= False
    print(task_from_db)
    
    db.commit()
    db.refresh(task_from_db)
    return task_from_db

@app.delete("/tasks/{task_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_task(task_id:str, db= Depends(get_db)):
    task_to_remove= db.get(TaskORM, task_id)
    db.delete(task_to_remove)
    db.commit()