from app import db
from datetime import datetime

class Transactions(db.Document):
    sourceAccount=db.StringField()
    destinationAccount=db.StringField()
    value=db.IntField()
    createdDate= db.DateTimeField(default=datetime.now)