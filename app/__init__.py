from flask import Flask
import os
from flask_mongoengine import MongoEngine
db = MongoEngine()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'transaction',
    'host': os.environ.get('MONGO_URI')
}

db = MongoEngine(app)

from app.controllers import transactionController
