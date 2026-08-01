from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise", 
        back_populates="exercise",
        cascade="all, delete-orphan")

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True
    )

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
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise", 
        back_populates="workout",
        cascade="all, delete-orphan"
       )

    exercises = db.relationship(
    "Exercise",
    secondary="workout_exercises",
    back_populates="workouts",
    viewonly=True
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
        if value and len(value) > 500:
            raise ValueError("Notes cannot exceed 500 characters.")
        return value

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column( db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    __table_args__ = (
        CheckConstraint("sets >= 0", name="check_sets"),
        CheckConstraint("reps >= 0", name="check_reps"),
        CheckConstraint("duration_seconds >= 0", name="check_duration_seconds"),
    )
    

    @validates("sets", "reps", "duration_seconds")
    def validate_numbers(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} cannot be negative.")
        return value

    
