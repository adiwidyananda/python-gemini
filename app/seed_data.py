from sqlalchemy.orm import Session
from app.database import get_db
from app import models

def seed_data(db: Session):
    users = [
        models.User(name="john doe", email="john.doe@example.com", hobby="Photography", job="Software Engineer", age=29),
        models.User(name="jane smith", email="jane.smith@example.com", hobby="Painting", job="Graphic Designer", age=34),
        models.User(name="alice brown", email="alice.brown@example.com", hobby="Hiking", job="Data Scientist", age=27),
        models.User(name="bob johnson", email="bob.johnson@example.com", hobby="Cycling", job="Marketing Manager", age=41),
        models.User(name="carol lee", email="carol.lee@example.com", hobby="Cooking", job="Teacher", age=38)
    ]
    db.add_all(users)
    db.commit()

if __name__ == "__main__":
    db=next(get_db())
    seed_data(db)
    db.close()