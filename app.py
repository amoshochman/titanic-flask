import pandas as pd
import matplotlib

matplotlib.use('agg') #check if in use
import matplotlib.pyplot as plt
from flask import Flask, send_file, jsonify
import os
from models import db, Passenger
from flask_restx import Api, Resource
import csv
from flask_restx import reqparse
import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute

from constants import PROJECT_ROOT, TITANIC_DATABASE

CUR_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ATTRIBUTES = 'attributes'
RAW_DATA = 'data'
TITANIC_CSV = 'titanic.csv'
HIST_PDF = 'hist.pdf'
TITANIC_DB = 'titanic.db'

app = Flask(__name__)
api = Api(app)


def as_dict(my_object, attributes_list=None):
    return {c.name: getattr(my_object, c.name) for c in my_object.__table__.columns if
            (not attributes_list or c.name in attributes_list)}


@api.route('/passengers')
class PassengersClass(Resource):
    def get(self):
        return jsonify([as_dict(passenger) for passenger in Passenger.query.all()])


@api.route('/histogram')
class Histogram(Resource):
    def get(self):
        csv_path = os.path.join(CUR_FOLDER, RAW_DATA, TITANIC_CSV)
        df = pd.read_csv(csv_path)
        ax = df.Fare.hist()
        fig = ax.get_figure()
        plt.show()
        image_path = os.path.join(CUR_FOLDER, RAW_DATA, HIST_PDF)
        fig.savefig(image_path)
        return send_file(image_path, mimetype='image/pdf')


parser = reqparse.RequestParser()
parser.add_argument(ATTRIBUTES, help="The desired attribute fields", required=False)


def get_passenger_attributes():
    passenger_attributes_tuples = inspect.getmembers(Passenger, lambda a: not (inspect.isroutine(a)))
    return {my_tuple[0] for my_tuple in passenger_attributes_tuples if isinstance(my_tuple[1], InstrumentedAttribute)}


def get_attributes_list(attributes):
    input_attributes_list = [elem.strip().capitalize() for elem in attributes.split()]
    invalid_attributes = {att for att in input_attributes_list if att not in get_passenger_attributes()}
    if invalid_attributes:
        raise ValueError("Invalid attribute/s:" + str(invalid_attributes))
    return input_attributes_list


@api.route('/passenger/<int:passenger_id>')
@api.doc(params={'passenger_id': 'The ID of a passenger'})
@api.expect(parser)
class PassengerClass(Resource):
    def get(self, passenger_id):
        args = parser.parse_args()
        attributes = args[ATTRIBUTES]
        if attributes:
            try:
                attributes_list = get_attributes_list(attributes)
            except ValueError as e:
                return str(e), 400
        else:
            attributes_list = None
        passenger = Passenger.query.get(passenger_id)
        if not passenger:
            return "No passenger found with id: " + str(passenger_id), 400
        return jsonify(as_dict(passenger, attributes_list=attributes_list))


def create_app(db_location):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app(f"sqlite:////{PROJECT_ROOT}/{TITANIC_DATABASE}")
    app.run(debug=True)
