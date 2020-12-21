from dogs import models, schemas
from sqlalchemy.orm import Session


def get_dogs(db: Session, skip: int = 0, limit: int = 100):
    """
    Method that return all dogs
    """
    return db.query(models.Dog).offset(skip).limit(limit).all()


def get_dog_by_name(db: Session, dog_name: str):
    """
    Method that return a dog by an specific name
    """
    return db.query(models.Dog).filter(models.Dog.name == dog_name).first()


def get_dog_is_adopted(db: Session, is_adopted: bool):
    """
    Method that returns all dogs by is_adopted status
    """
    return db.query(models.Dog).filter(models.Dog.is_adopted == is_adopted).all()


def create_dog(db: Session, dog: schemas.DogCreate):
    """
    Method that creat a new dog
    """
    db_dog = models.Dog(
        name=dog.name,
        picture=dog.picture,
        create_date=dog.create_date,
        is_adopted=dog.is_adopted
    )
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog


def update_dog(db: Session, dog_name: str, dog_update: schemas.DogCreate):
    """
    Method that update a dog by an specific name
    """
    dog_query = db.query(models.Dog).filter(models.Dog.name == dog_name).first()
    if dog_query:
        dog_query.name = dog_update.name
        dog_query.picture = dog_update.picture
        dog_query.create_date = dog_update.create_date
        dog_query.is_adopted = dog_update.is_adopted
        db.commit()
        db.refresh(dog_query)
        return dog_query
    else:
        return None


def delete_dog(db: Session, dog_name: str):
    """
    Method that deletes a dog by an specific name
    """
    dog_query = db.query(models.Dog).filter(models.Dog.name == dog_name).first()
    db.delete(dog_query)
    db.commit()
    return True