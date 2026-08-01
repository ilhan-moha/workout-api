from flask import Flask, jsonify, request
from flask_migrate import Migrate
import os
from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "instance","app.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)
#routes

@app.route("/")
def home():
    return {
        "message": "Welcome to the Workout Tracker API!"
    }, 200

#workout routes
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200

@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout), 200

@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    errors = workout_schema.validate(data)
    if errors:
        return errors, 400

    workout = Workout(
        date=data["date"],
        duration_minutes=data["duration_minutes"],
        notes=data.get("notes")
    )

    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201

@app.route("/workouts/<int:id>", methods=["PATCH"])
def update_workout(id):
    workout = Workout.query.get_or_404(id)
    data = request.get_json()

    if "date" in data:
        workout.date = data["date"]

    if "duration_minutes" in data:
        workout.duration_minutes = data["duration_minutes"]

    if "notes" in data:
        workout.notes = data["notes"]

    db.session.commit()

    return workout_schema.dump(workout), 200

@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return {"message": "Workout deleted successfully."}, 200

#exercise routes

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    errors = exercise_schema.validate(data)
    if errors:
        return errors, 400

    exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data["equipment_needed"]
    )

    db.session.add(exercise)
    db.session.commit()

    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:id>", methods=["PATCH"])
def update_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        exercise.name = data["name"]

    if "category" in data:
        exercise.category = data["category"]

    if "equipment_needed" in data:
        exercise.equipment_needed = data["equipment_needed"]

    db.session.commit()

    return exercise_schema.dump(exercise), 200


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    db.session.delete(exercise)
    db.session.commit()

    return {"message": "Exercise deleted successfully."}, 200


# workout exercise routes

@app.route("/workout-exercises", methods=["GET"])
def get_workout_exercises():
    workout_exercises = WorkoutExercise.query.all()
    return jsonify(workout_exercises_schema.dump(workout_exercises)), 200


@app.route("/workout-exercises/<int:id>", methods=["GET"])
def get_workout_exercise(id):
    workout_exercise = WorkoutExercise.query.get_or_404(id)
    return workout_exercise_schema.dump(workout_exercise), 200


@app.route("/workout-exercises", methods=["POST"])
def create_workout_exercise():
    data = request.get_json()

    errors = workout_exercise_schema.validate(data)

    if errors:
        return errors, 400

    workout_exercise = WorkoutExercise(
        workout_id=data["workout_id"],
        exercise_id=data["exercise_id"],
        sets=data.get("sets"),
        reps=data.get("reps"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return workout_exercise_schema.dump(workout_exercise), 201


@app.route("/workout-exercises/<int:id>", methods=["PATCH"])
def update_workout_exercise(id):
    workout_exercise = WorkoutExercise.query.get_or_404(id)

    data = request.get_json()

    if "sets" in data:
        workout_exercise.sets = data["sets"]

    if "reps" in data:
        workout_exercise.reps = data["reps"]

    if "duration_seconds" in data:
        workout_exercise.duration_seconds = data["duration_seconds"]

    db.session.commit()

    return workout_exercise_schema.dump(workout_exercise), 200


@app.route("/workout-exercises/<int:id>", methods=["DELETE"])
def delete_workout_exercise(id):
    workout_exercise = WorkoutExercise.query.get_or_404(id)

    db.session.delete(workout_exercise)
    db.session.commit()

    return {
        "message": "Workout exercise deleted successfully."
    }, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)