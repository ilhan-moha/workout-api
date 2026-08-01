from marshmallow import Schema, fields, validate, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min =3))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(validate=validate.Range(min=0))
    reps = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True, 
        validate=validate.Range(min=1))
    notes = fields.Str(
        validate=validate.Length(max=500))
    exercises = fields.Nested(
        WorkoutExerciseSchema,
          many=True, 
          dump_only=True)

    @validates("notes")
    def validate_notes(self, value):
        if value and value.strip() == "":
            raise ValidationError("Notes cannot be empty.")