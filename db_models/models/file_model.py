import mongoengine


class FilesModel(mongoengine.EmbeddedDocument):
    file = mongoengine.FileField()
