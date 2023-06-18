import pandas as pd
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
from flask import Flask, send_file, jsonify
import os
from models import db, Passenger
from flask_restx import Api, Resource
import csv
from flask_restx import reqparse
import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute

CUR_FOLDER = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ATTRIBUTES = 'attributes'
RAW_DATA = 'data'
TITANIC_CSV = 'titanic.csv'


def as_dict(my_object, attributes_list=None):
    return {c.name: getattr(my_object, c.name) for c in my_object.__table__.columns if
            (not attributes_list or c.name in attributes_list)}


app = Flask(__name__)
api = Api(app)

ns = api.namespace("todos", description="TODO operations")


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
        image_path = os.path.join(CUR_FOLDER, RAW_DATA, 'hist.pdf')
        fig.savefig(image_path)
        return send_file(image_path, mimetype='image/pdf')


parser = reqparse.RequestParser()
parser.add_argument(ATTRIBUTES, help="The desired attribute fields", required=False)


def get_attributes_list(attributes):
    input_attributes_list = [elem.strip().capitalize() for elem in attributes.split()]
    cleaned_list = []
    passenger_attributes_tuples = inspect.getmembers(Passenger, lambda a: not (inspect.isroutine(a)))
    passenger_attributes_names = [elem[0] for elem in passenger_attributes_tuples]
    for elem in input_attributes_list:
        if elem in passenger_attributes_names:
            elem_type = [some_tuple for some_tuple in passenger_attributes_tuples if some_tuple[0] == elem][0][1]
            if not isinstance(elem_type, InstrumentedAttribute):
                raise ValueError("Invalid attribute:" + elem)
            cleaned_list.append(elem)
        else:
            raise ValueError("Invalid attribute:" + elem)
    return cleaned_list


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
        passenger = Passenger.query.get(passenger_id)
        if not passenger:
            return "No passenger found with id: " + str(passenger_id), 400
        return jsonify(as_dict(passenger, attributes_list=attributes_list))


def populate_db():
    csv_path = os.path.join(CUR_FOLDER, RAW_DATA, TITANIC_CSV)
    with open(csv_path) as f:
        reader = csv.reader(f)
        _ = next(reader)
        for i, data in enumerate(reader):
            passenger = Passenger(*data)
            db.session.add(passenger)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db_file = os.environ.get('TITANIC_DB') or 'titanic.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.create_all()
        if not Passenger.query.first():
            populate_db()
    app.run(debug=True)
