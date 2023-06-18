from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Passenger(db.Model):
    PassengerId = db.Column(db.Integer, primary_key=True)
    Survived = db.Column(db.Integer)
    Pclass = db.Column(db.Integer)
    Name = db.Column(db.String)
    Sex = db.Column(db.String)
    Age = db.Column(db.Integer)
    SibSp = db.Column(db.Integer)
    Parch = db.Column(db.Integer)
    Ticket = db.Column(db.String)
    Fare = db.Column(db.Float)
    Cabin = db.Column(db.String)
    Embarked = db.Column(db.String)

    def __init__(self, PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked):
        self.PassengerId = PassengerId
        self.Survived = Survived
        self.Pclass = Pclass
        self.Name = Name
        self.Sex = Sex
        self.Age = Age
        self.SibSp = SibSp
        self.Parch = Parch
        self.Ticket = Ticket
        self.Fare = Fare
        self.Cabin = Cabin
        self.Embarked = Embarked




