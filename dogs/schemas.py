from typing import List, Optional
from pydantic import BaseModel


class DogBase(BaseModel):
    name: str
    picture: str
    create_date: str
    is_adopted: bool


class DogCreate(DogBase):
    pass


class Dog(DogBase):
    id: str

    class Config:
        orm_mode = True
