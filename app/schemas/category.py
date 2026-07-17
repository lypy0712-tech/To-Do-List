from pydantic import BaseModel, ConfigDict

class CategoryBaseSchema(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)

class CategorySchema(BaseModel):
    name: str
    
    model_config = ConfigDict(from_attributes=True)
