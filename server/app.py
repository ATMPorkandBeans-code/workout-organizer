from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

#Gets all exercises
@app.route('/exercises')
def get_exercises():
    exercises = Exercise.query.all()

    if not exercises:
        return make_response({"error": "Exercises not found"})
    try:
        result = ExerciseSchema(many=True).dump(exercises)
    except ValidationError as err:
        return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400
    
    return make_response(result)

#Gets exercises at their ID number
@app.route('/exercises/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.filter(Exercise.id == id).first()

    if not exercise:
        return make_response({"error": "Exercise not found"}), 404 
    try:
        result = ExerciseSchema().dump(exercise)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400

    return (make_response(result))

#Posts new exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    query_results = db.session.execute(db.select(Exercise.id)).all()
    if not query_results:
        new_id = 1
    else:
        id_list = [r.id for r in query_results]
        new_id = max(id_list) + 1

    try:
        validated = ExerciseSchema().load(data)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400
        

    new_exercise = Exercise(**validated)
    new_exercise.id = new_id

    db.session.add(new_exercise)
    db.session.commit()
    
    try:
        result = ExerciseSchema().dump(new_exercise)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400
    return make_response(result), 201

#Deletes an exercise at it's ID
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({'message': f'Exercise with id {id} deleted successfully'}), 200

#Gets all workouts
@app.route('/workouts')
def get_workouts():
    workouts = Workout.query.all()

    if not workouts:
        return make_response({"error": "Workouts not found"}) 
    try:
        result = WorkoutSchema(many=True).dump(workouts)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400

    return make_response(result)

#Gets workout at it's ID
@app.route('/workouts/<int:id>')
def get_workout(id):
    workout = Workout.query.filter(Workout.id == id).first()

    if not workout:
        return make_response({"error": "Workout not found"}), 404
    try:
        result = WorkoutSchema().dump(workout)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400
    
    return (make_response(result))

#Posts a new workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    query_results = db.session.execute(db.select(Workout.id)).all()
    if not query_results:
        new_id = 1
    else:
        id_list = [r.id for r in query_results]
        new_id = max(id_list) + 1
    try:
        validated = WorkoutSchema().load(data)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400

    new_workout = Workout(**validated)
    new_workout.id = new_id
    
    db.session.add(new_workout)
    db.session.commit()
    try:
        result = WorkoutSchema().dump(new_workout)
    except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400
    return make_response(result), 201

#Deletes a workout 
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return make_response({'message': f'Workout with id {id} deleted successfully'}), 200

#Adds an exercise to a workout with the number of sets, reps and duration of seconds
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
     data = request.get_json()
     workout = Workout.query.filter_by(id=workout_id).first()
     exercise = Exercise.query.filter_by(id=exercise_id).first()

     if not workout:
        return make_response({"error": "Workout not found"}), 404
     
     if not exercise:
        return make_response({"error": "Exercise not found"}), 404

     query_results = db.session.execute(db.select(WorkoutExercise.id)).all()
     if not query_results:
        new_id = 1
     else:
        id_list = [r.id for r in query_results]
        new_id = max(id_list) + 1

     new_workout_exercise = WorkoutExercise(id=new_id,
                                            workout_id=workout.id,
                                            exercise_id=exercise.id,
                                            reps=data['reps'],
                                            sets=data['sets'],
                                            duration_seconds=data['duration_seconds'])
     db.session.add(new_workout_exercise)
     db.session.commit()
     try:
        result = WorkoutExerciseSchema().dump(new_workout_exercise)
     except ValidationError as err:
            return make_response({
            "valid_data": err.valid_data,
            "errors": err.messages
        }), 400
     return make_response(result), 201



if __name__ == '__main__':
    app.run(port=5555, debug=True)