from app import fill_csv_dict
from utils import get_passenger_attributes
from models import Passenger, db



def test_passengers(client):
    response = client.get("/passengers")
    assert response.status_code == 200
    assert type(response.json) == list and len(response.json) == 891
    response_with_db = response.json
    passenger_attributes = get_passenger_attributes()
    assert (all(row.keys() == passenger_attributes for row in response.json))
    name = "Peter Cantropus"
    age = 99
    id = max(elem['PassengerId'] for elem in response.json) + 1
    passenger = Passenger(PassengerId=id, Name=name, Age=age)
    db.session.add(passenger)
    db.session.commit()
    response = client.get("/passenger/" + str(id))
    assert (response.json.keys() == passenger_attributes)
    response = client.get("/passenger/" + str(id) + "?attributes=age%20name")
    assert response.json == {"Age": age, "Name":name}
    some_id = "10"
    response = client.get("/passenger/" + some_id)
    response_passenger_with_db = response.json
    fill_csv_dict()
    response = client.get("/passengers")
    response_with_csv = response.json
    assert response_with_csv == response_with_db
    response = client.get("/passenger/" + some_id)
    response_passenger_with_csv = response.json
    assert response_passenger_with_csv == response_passenger_with_db








