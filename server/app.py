from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Define Routes here
@app.route('/exercises')
def get_exercises():
    all_exercises = []
    exercises = Exercise.query.all()

    if not exercises:
        return make_response({"error": "Exercises not found"})

    for exercise in exercises:
            exercise_dict = {
                'id': exercise.id,
                'name': exercise.name,
                'category': exercise.category,
                'equipment_needed': exercise.equipment_needed
            }
            all_exercises.append(exercise_dict)
    return make_response(all_exercises)


@app.route('/exercise/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()

    if not exercise:
        return make_response({"error": "Exercise not found"}), 404
    
    body = {'id': exercise.id,
            'name': exercise.name,
            'category': exercise.category,
            'equipment_needed': exercise.equipment_needed
            }

    return (make_response(body))


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    query_results = db.session.execute(db.select(Exercise.id)).all()
    id_list = [r.id for r in query_results]
    new_id = max(id_list) + 1
    new_exercise = Exercise(id=new_id,
                            name=data.name,
                            category=data.category,
                            equipment_needed=data.equipment_needed)
    db.session.add(new_exercise)
    db.session.commit()
    return make_response({'id': new_exercise.id,
                           'name': new_exercise.name,
                           'category': new_exercise.category,
                           'equipment_needed': new_exercise.equipment_needed
                           }), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({'message': f'Exercise with id {id} deleted successfully'}), 200


@app.route('/workouts')
def get_workouts():
    all_workouts = []
    workouts = Workout.query.all()

    if not workouts:
        return make_response({"error": "Workouts not found"})

    for workout in workouts:
            workout_dict = {
                'id': workout.id,
                'date ': workout.date,
                'duration_minutes': workout.duration_minutes,
                'notes': workout.notes
            }
            all_workouts.append(workout_dict)
    return make_response(all_workouts)


@app.route('/workouts/<int:id>')
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()

    if not workout:
        return make_response({"error": "Workout not found"}), 404
    
    body = {'id': workout.id,
            'date ': workout.date,
            'duration_minutes': workout.duration_minutes,
            'notes': workout.notes
            }

    return (make_response(body))


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    query_results = db.session.execute(db.select(Workout.id)).all()
    id_list = [r.id for r in query_results]
    new_id = max(id_list) + 1
    new_workout = Workout(id=new_id,
                            date=data.date,
                            duration_minutes=data.duration_minutes,
                            notes=data.notes)
    db.session.add(new_workout)
    db.session.commit()
    return make_response({'id': new_workout.id,
                           'date': new_workout.date,
                           'duration_minutes': new_workout.duration_minutes,
                           'notes': new_workout.notes
                           }), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return make_response({'message': f'Workout with id {id} deleted successfully'}), 200


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
     data = request.get_json()
     workout = Workout.query.filter_by(id=workout_id).first()
     exercise = Exercise.query.filter_by(id=exercise_id).first()

     query_results = db.session.execute(db.select(WorkoutExercise.id)).all()
     id_list = [r.id for r in query_results]
     new_id = max(id_list) + 1

     new_workout_exercise = WorkoutExercise(id=new_id,
                                            workout_id=workout.id,
                                            exercise_id=exercise.id,
                                            reps=data.reps,
                                            set=data.sets,
                                            duration_seconds=data.duration_seconds)
     db.session.add(new_workout_exercise)
     db.session.commit()
     return make_response({'id': new_workout_exercise.id,
                           'workout_id': new_workout_exercise.workout_id,
                           'exercise_id': new_workout_exercise.exercise_id,
                           'reps': new_workout_exercise.reps,
                           'sets': new_workout_exercise.sets,
                           'duration_seconds': new_workout_exercise.duration_seconds
                           }), 201






if __name__ == '__main__':
    app.run(port=5555, debug=True)