from fastapi import APIRouter, status, Depends, HTTPException

from app.api.dependencies import get_category_service
from app.services.category import CategoryServices, CategoryNotFound
from app.schemas.category import CategorySchema, CategoryBaseSchema
router = APIRouter(prefix = "/categories", tags=["Categories"])

@router.get("", status_code=status.HTTP_200_OK)
def read_category(category_services: CategoryServices= Depends(get_category_service)) -> list[CategoryBaseSchema]:
    return category_services.list_category()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategorySchema, 
                    category_services: CategoryServices= Depends(get_category_service)) -> CategoryBaseSchema:
    return category_services.create_category(category_create=payload)

@router.patch("/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id:str, payload: CategorySchema, 
                    category_services: CategoryServices= Depends(get_category_service)) -> CategoryBaseSchema:
    try:
        return category_services.update_category(category_id, payload)
    except(CategoryNotFound):
        HTTPException(status_code=404, detail="Category not found")

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_services: CategoryServices= Depends(get_category_service)) -> None:
    try:
        category_services.delete_category(category_id)
    except(CategoryNotFound):
        HTTPException(status_code=404, detail="Category not found")