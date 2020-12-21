from sqlalchemy import Boolean, String, Column, UniqueConstraint
from database import Base


def generate_id():
    from uuid import uuid4
    return str(uuid4())


class Dog(Base):
    """
        Dog model to create a new dog information
    """
    __tablename__ = "dogs"

    id = Column(String, primary_key=True, index=True, nullable=False, default=generate_id)
    name = Column(String, unique=False, index=True)
    picture = Column(String, unique=True)
    create_date = Column(String, default=False)
    is_adopted = Column(Boolean)
