# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if not earthquake:
        response_body = {"message": f"Earthquake {id} not found."}
        return make_response(jsonify(response_body), 404)
    
    response_body = {
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    }
    return make_response(jsonify(response_body), 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes_list = []
    for quake in earthquakes:
        quakes_list.append({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        })
    
    response_body = {
        "count": len(earthquakes),
        "quakes": quakes_list
    }
    return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
