import flask
from flask import jsonify
from flask import request
from sql import create_connection
from sql import execute_read_query
import creds

# setting up an application name
app = flask.Flask(__name__)  # sets up the application
app.config["DEBUG"] = True  # allow to show errors in browser

cars = [
    {'id': 0,
     'make': 'Jeep',
     'model': 'Cherokee',
     'year': '2000',
     'color': 'black'},
    {'id': 1,
     'make': 'Ford',
     'model': 'Mustang',
     'year': '1970',
     'color': 'white'},
    {'id': 2,
     'make': 'Dodge',
     'model': 'Challenger',
     'year': '2020',
     'color': 'red'}
]


@app.route('/', methods=['GET'])  # default url without any routing
def home():
    return "<h1>WELCOME TO OUR FIRST API</h1>"

@app.route('/api/car/all', methods=['GET']) #get all the cars
def api_all():
    return jsonify(cars)

#http://127.0.0.1:5000/api/car?id=1
@app.route('/api/car', methods=['GET']) #get a single car by id
def api_id():
    if 'id' in request.args: #only if an id is provided, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: no ID provided'
    results = [] #resulting car(s) to return
    for car in cars:
        if car['id'] == id:
            results.append(car)
    return jsonify(results)

@app.route('/api/car', methods=['POST']) #add a car
def add_example():
    request_data = request.get_json()
    newid = request_data['id']
    newmake = request_data['make']
    newmodel = request_data['model']
    newyear = request_data['year']
    newcolor = request_data['color']

    cars.append({'id': newid, 'make': newmake, 'model': newmodel, 'year': newyear, 'color': newcolor})
    return 'Add request successful!'

@app.route('/api/car', methods=['DELETE']) #delete a car
def delete_example():
    request_data = request.get_json()
    idToDelete = request_data['id']
    for i in range(len(cars) -1, -1, -1): #start, stop, step size
        if cars[i]['id'] == idToDelete:
            del(cars[i])
    return "delete request successful"

@app.route('/api/users', methods=['GET']) #api to get users from the db table in AWS by id in JSON response
def api_users_id():
    if 'id' in request.args: #only if an id is provided, proceed
        id = int(request.args['id'])
    else:
        return 'ERROR: NO ID provided'

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM users"
    users = execute_read_query(conn, sql)
    results = []

    for user in users:
        if user['id'] == id:
            results.append(user)
    return jsonify(results)





app.run()
