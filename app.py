import csv

import pandas as pd
import matplotlib

from utils import as_dict, get_attributes_list, use_db, get_number_or_string

matplotlib.use('agg')
import matplotlib.pyplot as plt
from flask import Flask, send_file, jsonify
import os
from models import Passenger, db
from flask_restx import Api, Resource
from flask_restx import reqparse

from constants import PROJECT_ROOT, TITANIC_DATABASE, ATTRIBUTES, RAW_DATA, HIST_PDF, TITANIC_CSV

app = Flask(__name__)
api = Api(app)
csv_dict = {}


@api.route('/passengers')
class PassengersClass(Resource):
    def get(self):
        if csv_dict:
            return jsonify(list(csv_dict.values()))
        return jsonify([as_dict(passenger) for passenger in Passenger.query.all()])


@api.route('/histogram')
class Histogram(Resource):
    def get(self):
        if csv_dict:
            df = pd.DataFrame.from_dict(csv_dict).T
        else:
            my_list = [as_dict(passenger) for passenger in Passenger.query.all()]
            df = pd.DataFrame.from_records(my_list)
        ax = df.Fare.hist()
        fig = ax.get_figure()
        plt.show()
        image_path = os.path.join(PROJECT_ROOT, RAW_DATA, HIST_PDF)
        fig.savefig(image_path)
        return send_file(image_path, mimetype='image/pdf')


parser = reqparse.RequestParser()
parser.add_argument(ATTRIBUTES, help="The desired attribute fields", required=False)


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
        passenger = csv_dict[passenger_id] if csv_dict else Passenger.query.get(passenger_id)
        if not passenger:
            return "No passenger found with id: " + str(passenger_id), 400
        return jsonify(as_dict(passenger, attributes_list=attributes_list))


def fill_csv_dict():
    csv_path = os.path.join(PROJECT_ROOT, RAW_DATA, TITANIC_CSV)
    myFile = open(csv_path, 'r')
    reader = csv.DictReader(myFile)
    for dictionary in reader:
        csv_dict[int(dictionary['PassengerId'])] = {k: (get_number_or_string(v) if k != "Ticket" else v) for k, v in
                                                    dictionary.items()}

def create_app(db_location):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location
    db.init_app(app)
    return app


if __name__ == '__main__':
    if use_db():
        app = create_app(f"sqlite:////{PROJECT_ROOT}/{TITANIC_DATABASE}")
    else:
         fill_csv_dict()
    app.run(debug=True)
