from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from marshmallow import Schema, fields

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    @validates('category')
    def validate_category(self, key, value):
        if value not in ["Cardio", "Weight Training", "Body Weight Exercise", ]:
            raise ValueError("Category must be available")
        return value

    workout_exercises = db.relationship('WorkoutExercise', back_populates = 'exercise')
    workouts = association_proxy('workout_exercises', 'workout', creator=lambda workout_obj: WorkoutExercise(workout=workout_obj))
     
    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}>'
    
class ExerciseSchema(Schema):
    id = fields.Int()
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("exercise",))))


class Workout(db.Model):
    __tablename__ = 'workouts'

    id =  db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text, CheckConstraint("LENGTH(notes) <= 200", name="notes_length_check"))

    @validates('duration_minutes')
    def validate_workout_details(self, key, value):
        if value <= 0:
            raise ValueError('Value must be a positive integer')
        return value

    workout_exercises = db.relationship('WorkoutExercise', back_populates = 'workout')
    exercises = association_proxy('workout_exercises', 'exercise', creator=lambda exercise_obj: WorkoutExercise(exercise=exercise_obj))

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}>'
    
class WorkoutSchema(Schema):
    id = fields.Integer()
    date = fields.Date()
    duration_minutes = fields.Integer()
    notes = fields.String()

    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout",))))


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id =  db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer,db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer,db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    @validates('reps', 'sets', 'duration_seconds')
    def validate_workout_details(self, key, value):
        if value <= 0:
            raise ValueError('Value must be a positive integer')
        return value

    exercise = db.relationship('Exercise', back_populates = 'workout_exercises')
    workout = db.relationship('Workout', back_populates = 'workout_exercises')

    def __repr__(self):
        return f'<WorkoutExercise {self.id}, {self.reps}, {self.sets}, {self.duration_seconds}>'

class WorkoutExerciseSchema(Schema):

    id = fields.Integer()
    reps = fields.Integer()
    sets = fields.Integer()
    duration_seconds = fields.Integer()

    exercise = fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises',)))
    workout = fields.Nested(lambda: WorkoutSchema(exclude=('workout_exercises',)))







