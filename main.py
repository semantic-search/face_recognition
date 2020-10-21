from db_models.models.cache_model import Cache
from db_models.models.face_model import FaceModel
import uuid
from db_models.mongo_setup import global_init
import init
import globals
import requests


def recog_face(image):
    url = globals.FACE_RECOG_SERVER
    files = [
        ('file', open(image, 'rb'))
    ]
    response = requests.request("POST", url, files=files)
    person = response.text.encode('utf8')
    if person:
        return person
    else:
        return False


if __name__ == "__main__":
    global_init()
    print('main fxn')
    for message in init.consumer_obj:
        print(message)
        message = message.value
        db_key = str(message)

        db_object = Cache.objects.get(pk=db_key)
        try:
            file_name = db_object.file_name
            init.redis_obj.set(globals.RECEIVE_TOPIC, file_name)
            print('after redis')
            if db_object.is_doc_type:
                """document"""
                print('in doc type')
                images_array = []
                faces = []
                for cache_obj in db_object.files:
                    face_model_object = FaceModel()
                    file_id = cache_obj.file
                    face_model_object.file = file_id
                    face_model_object.document = cache_obj
                    pdf_image = str(uuid.uuid4()) + ".jpg"
                    with open(pdf_image, 'wb') as file_to_save:
                        file_to_save.write(cache_obj.file.read())
                    face = recog_face(pdf_image)
                    face_model_object.person = face
                    face_model_object.save()
                    faces.append(face)
                db_object.faces = faces
                db_object.save()
            else:
                """image"""
                print('in image type')
                file_id = db_object.file
                with open(file_name, 'wb') as file_to_save:
                    file_to_save.write(db_object.file.read())
                face_model_object = FaceModel()
                face_model_object.file = file_id
                face_model_object.document = db_object
                face = recog_face(file_name)
                db_object.faces = [face]
                face_model_object.save()
                db_object.save()
        except Exception as e:
            print(e)
