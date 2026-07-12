from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api.routers.task import router as task_router
from app.models.base import Base
from app.db.session import engine
from app.core.config import get_settings

settings= get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title= "My To-Do-List",
    lifespan=lifespan
)

app.include_router(router=task_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.cors_allowed_origin,
    allow_methods= ["*"],
    allow_headers=['*']
)


