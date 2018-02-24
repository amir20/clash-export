from datetime import datetime

import pickle
from mongoengine import BinaryField, DateTimeField, Document, StringField


class TrainedModel(Document):
    name = StringField(required=True, unique=True)
    last_updated = DateTimeField(default=datetime.now)
    model_bytes = BinaryField(required=True)
    meta = {
        'index_background': True,
        'indexes': [
            'name',
        ]
    }

    @property
    def model(self):
        return pickle.loads(self.model_bytes)

    @model.setter
    def model(self, model):
        self.model_bytes = pickle.dumps(model)
