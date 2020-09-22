import mongoengine
import datetime

from mongoengine.fields import FloatField


class People(mongoengine.Document):
    """Main model"""
    name = mongoengine.StringField(required=True)
    """Name of the person"""
    encoding = mongoengine.ListField(FloatField())
    """encoding of image"""

    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    meta = {
        'db_alias': 'core',
    }
