from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    muscle_group = db.Column(db.String, nullable=False)

workout_exercises = db.relationship(
    "WorkoutExercise", back_populates="exercise",
      cascade="all, delete-orphan")

__table_args__ = (
    checkConstraint("length(name) > 0", name = "check_exercise_name"),

)

@validates("name")
def validate_name(self, key, value):
    if len(value.strip()) < 3:
        raise ValueError("Exercise name must be at least 3 characters long.")
    return value.strip()

@validates("category")
def validate_category(self, key, value):
    if not value.strip():
        raise ValueError("Category cannot be empty.")
    return value.strip()