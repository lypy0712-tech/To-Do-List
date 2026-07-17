from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import CategorySchema, CategoryBaseSchema
class CategoryNotFound(Exception):
    """if category ID not found"""


class CategoryServices:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_category(self) -> list[CategoryBaseSchema]:
        category_orm = self.category_repository.get_all()
        return [CategoryBaseSchema.model_validate(category) for category in category_orm]
    
    def create_category(self, category_create: CategorySchema) -> CategoryBaseSchema:
        category_orm = self.category_repository.create(name=category_create.name)
        self.db.commit()
        return CategoryBaseSchema.model_validate(category_orm)
    
    def update_category(self, id: str, category_update: CategorySchema) -> CategoryBaseSchema:
        category_for_update = self.category_repository.get_by_id(id)
        if category_for_update is None:
            raise CategoryNotFound(f"Category with ID {id} not found")
        
        category_for_update.name = category_update.name
            
        self.db.commit()
        return category_for_update

    def delete_category(self, category_id: str) -> None:
        category_for_delete =  self.category_repository.get_by_id(category_id)
        if category_for_delete is None:
            raise CategoryNotFound(f"Category  with ID {category_id} not found")
        self.db.delete(category_for_delete)
        self.db.commit()