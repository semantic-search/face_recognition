import mongoengine
import globals


def global_init():
    mongoengine.register_connection(
        db=globals.DB,
        host=globals.MONGO_HOST,
        port=int(globals.PORT),
        alias='core',
        authentication_source=globals.DB,
        username=globals.MONGO_USER,
        password=globals.MONGO_PASSWORD
    )
    mongoengine.connect(
        db=globals.DB,
        host=globals.MONGO_HOST,
        port=int(globals.PORT),
        username=globals.MONGO_USER,
        password=globals.MONGO_PASSWORD
    )

