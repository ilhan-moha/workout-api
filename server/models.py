from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
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
    CheckConstraint("length(name) >= 3", name="check_exercise_name"),
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

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String, nullable=True)

    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="check_duration"),
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError( "duration must be greater than 0.")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value and len(value) < 500:
            raise ValueError("Notes cannot exceed 500 characters.")
        return value