from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercise', back_populates = 'exercise')
    workouts = association_proxy('workout_exercises', 'workout', creator=lambda workout_obj: WorkoutExercise(workout=workout_obj))

class Workout(db.Model):
    __tablename__ = 'workouts'

    id =  db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates = 'workout')
    exercises = association_proxy('workout_exercises', 'exercise', creator=lambda exercise_obj: WorkoutExercise(exercise=exercise_obj))


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id =  db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer,db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer,db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    exercise = db.relationship('Exercise', back_populates = 'workout_exercises')
    workout = db.relationship('Workout', back_populates = 'workout_exercises')







