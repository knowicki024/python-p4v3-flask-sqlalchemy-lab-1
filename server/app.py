# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
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
def quake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if earthquake is None:
        response_body = {'message': f'Earthquake {id} not found.'}

        return make_response(response_body, 404)
    
    response_body = {
        'id': earthquake.id,
        'location': earthquake.location, 
        'magnitude':earthquake.magnitude, 
        'year': earthquake.year
    }
    return make_response(response_body, 200)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def quake_by_mag(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    earthquake_data = [{
        'id': eq.id,
        'location': eq.location,
        'magnitude': eq.magnitude,
        'year' : eq.year
    } for eq in earthquakes]

    response_body = {
        'count': len(earthquakes),
        'quakes': earthquake_data
    }
    return make_response(response_body, 200)



    
# Add views here


if __name__ == '__main__':
    app.run(port=5555, debug=True)
