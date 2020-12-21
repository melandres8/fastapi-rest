from typing import List
from requests import get
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from dogs import crud, models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """
    Dependency
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/dogs", response_model=List[schemas.Dog])
def get_a_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_dogs = crud.get_dogs(db, skip=skip, limit=limit)
    if db_dogs:
        return db_dogs
    else:
        raise HTTPException(status_code=404, detail="No dogs registered!")


@app.get("/api/dogs/{name}", response_model=schemas.Dog)
def get_by_name(dog_name: str, db: Session = Depends(get_db)):
    db_dog = crud.get_dog_by_name(db, dog_name=dog_name)
    if db_dog:
        return db_dog
    else:
        raise HTTPException(status_code=404, detail="Dog not found!")


@app.get("/api/dogs/is_adopted", response_model=List[schemas.Dog])
def get_adopted_dogs(is_adopted: bool = True, db: Session = Depends(get_db)):
    db_dogs = crud.get_dog_is_adopted(db, is_adopted=is_adopted)
    if db_dogs is None:
        raise HTTPException(status_code=404, detail="There's no adopted dogs!")
    else:
        return db_dogs


@app.post("/api/dogs/{name}", response_model=schemas.Dog)
def post_dog(dog: schemas.DogCreate, db: Session = Depends(get_db)):
    db_dog = crud.get_dog_by_name(db, dog_name=dog.name)
    if db_dog:
        raise HTTPException(status_code=400, detail="Dog name already exists!")
    else:
        picture = get('https://dog.ceo/api/breeds/image/random').json()
        dog.picture = picture.get('message')
        dog.create_date = datetime.now()
        crud.create_dog(db=db, dog=dog)
