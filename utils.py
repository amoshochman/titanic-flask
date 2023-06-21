import configparser
import inspect

from sqlalchemy.orm import InstrumentedAttribute

from constants import HOST_STRING, USE_DB_STRING
from models import Passenger


def as_dict(my_object, attributes_list=None):
    if type(my_object) == dict:
        return {k: v for k, v in my_object.items() if (not attributes_list or k in attributes_list)}
    return {c.name: getattr(my_object, c.name) for c in my_object.__table__.columns if
            (not attributes_list or c.name in attributes_list)}


def get_passenger_attributes():
    passenger_attributes_tuples = inspect.getmembers(Passenger, lambda a: not (inspect.isroutine(a)))
    return {my_tuple[0] for my_tuple in passenger_attributes_tuples if isinstance(my_tuple[1], InstrumentedAttribute)}


def get_attributes_list(attributes):
    input_attributes_list = [elem.strip().capitalize() for elem in attributes.split()]
    invalid_attributes = {att for att in input_attributes_list if att not in get_passenger_attributes()}
    if invalid_attributes:
        raise ValueError("Invalid attribute/s:" + str(invalid_attributes))
    return input_attributes_list


def get_config():
    config_dict = {}
    config = configparser.ConfigParser()
    config.read('config.ini')
    source = config.get('DATA', 'source', fallback="db")
    try:
        assert source in ('db', 'csv')
    except:
        raise ValueError("Invalid configuration given. File config.ini[DATA][source] should be either 'db' or 'csv'")
    config_dict[USE_DB_STRING] = True if source == 'db' else False
    config_dict[HOST_STRING] = config.get('NETWORK', 'host', fallback="localhost")
    return config_dict


def get_number_or_string(string):
    try:
        my_float = float(string)
        return int(string) if string.isnumeric() else my_float
    except ValueError:
        return string
