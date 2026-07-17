from .base import Base
from sqlalchemy.orm import Mapped, mapped_column


class CategoriesORM(Base):
    __tablename__ = "categories"
    
    name: Mapped[str]