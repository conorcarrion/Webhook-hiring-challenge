from app import db

# Database object to allow insertion of webhook information into sql database
class ChangeEvent(db.Model):
    __tablename__ = "changes"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<Change Event Data = {}>".format(self.data)
