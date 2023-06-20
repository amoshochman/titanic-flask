from app import get_passenger_attributes
from models import Passenger, db


def test_passengers(client):
    response = client.get("/passengers")
    assert response.status_code == 200
    assert type(response.json) == list and len(response.json) == 891
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








