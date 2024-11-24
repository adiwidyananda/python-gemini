from sqlalchemy.orm import Session
from . import models

# Get a user by name
def get_user(db: Session, name: str):
    return db.query(models.User).filter(models.User.name.like(f"%{name}%")).first()