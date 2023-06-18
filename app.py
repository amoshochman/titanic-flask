#import pandas as pd

from flask import Flask, request, Response, send_file, jsonify
import logging
import os
from models import db, Passenger
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask_restx import Api, Resource
import csv

def as_dict(my_object):
    return {c.name: getattr(my_object, c.name) for c in my_object.__table__.columns}

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return 'hello'

@api.route('/passengers')
class PassengersClass(Resource):
    def get(self):
        return jsonify([as_dict(passenger) for passenger in Passenger.query.all()])

@api.route('/histogram')
class Histogram(Resource):
    def get(self):
        if request.args.get('type') == '1':
           filename = 'ok.gif'
        else:
           filename = 'tree.jpg'
        return send_file(filename, mimetype='image/gif')


@api.route('/passenger/<int:passenger_id>')
class PassengerClass(Resource):
    def get(self, passenger_id):
        return jsonify(as_dict(Passenger.query.get(passenger_id)))


@api.route('/upload', methods=['POST'])
class HelloWorld2(Resource):
    def post(self):
        populate_db()
        return "ok"


def populate_db():
    cur_folder = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    csv_path = os.path.join(cur_folder, 'raw_data', 'titanic.csv')
    with open(csv_path) as f:
        reader = csv.reader(f)
        _ = next(reader)
        for i, data in enumerate(reader):
            passenger = Passenger(*data)
            db.session.add(passenger)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db_file = os.environ.get('FLIGHTS_DB') or 'titanic.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.create_all()
        if not Passenger.query.first():
            #todo: add try except ... if the data is corrupted, then nothing is added
            populate_db()
    app.run(debug=True)

