import mongoengine
from mongoengine import signals
import globals
import pickle

class UserModel(mongoengine.Document):
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        globals.add_to_embeddings(username= document.user_name, encoding=pickle.loads(document.encoding))
    user_name = mongoengine.StringField(required=True)
    full_name = mongoengine.StringField(required=True)
    img = mongoengine.FileField(required=True)
    encoding = mongoengine.BinaryField(required=True)
    meta = {
        'db_alias': 'core',
        'collection': 'face-recog'
    }
signals.pre_save.connect(UserModel.pre_save, sender=UserModel)
