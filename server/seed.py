from app import app
from models import *
from datetime import date

with app.app_context():

    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercise.query.delete()

    exercise1 = Exercise(id=1, name="Flat Push", category="Lift", equipment_needed=False)
    exercise2 = Exercise(id=2, name="Hammer Throw", category="Lift", equipment_needed=True)
    exercise3 = Exercise(id=3, name="Run", category="Cardio", equipment_needed=True)
    exercise4 = Exercise(id=4, name="Push Up", category="Cardio", equipment_needed=True)

    db.session.add_all([exercise1, exercise2, exercise3, exercise4])
    db.session.commit()


    workout1 = Workout(id=1, date=date(2025, 11, 12), duration_minutes=90, notes="Got a great sweat in, no notes")
    workout2 = Workout(id=2, date=date(2025, 9, 29), duration_minutes=60, notes="Feel Great!!!")
    workout3 = Workout(id=3, date=date(2025, 12, 29), duration_minutes=120, notes="Getting ready for the new year!")

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    db.session.add(WorkoutExercise(id=1, reps=20, sets=5, duration_seconds=60, exercise=exercise1, workout=workout2))
    db.session.add(WorkoutExercise(id=2, reps=30, sets=3, duration_seconds=60, exercise=exercise3, workout=workout1))
    db.session.add(WorkoutExercise(id=3, reps=15, sets=3, duration_seconds=120, exercise=exercise4, workout=workout3))
    db.session.add(WorkoutExercise(id=4, reps=10, sets=4, duration_seconds=30, exercise=exercise1, workout=workout1))
    db.session.add(WorkoutExercise(id=5, reps=25, sets=2, duration_seconds=90, exercise=exercise2, workout=workout2))
    db.session.commit()




