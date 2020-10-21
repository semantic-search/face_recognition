from db_models.models.cache_model import Cache
from db_models.models.face_model import FaceModel
import uuid
from db_models.mongo_setup import global_init
import init
import globals
import requests
import pyfiglet
import os

global_init()


def recog_face(image):
    print(image)
    url = globals.FACE_RECOG_SERVER
    print(url)
    files = [
        ('file', open(image, 'rb'))
    ]
    response = requests.request("POST", url, files=files)
    person = str(response.text)
    print("PERSON", person)
    if person == "false":
        return False
    else:
        return person


if __name__ == "__main__":
    print(pyfiglet.figlet_format(str(globals.RECEIVE_TOPIC)))
    print(pyfiglet.figlet_format("BULK FACE"))
    print(pyfiglet.figlet_format("INDEXER"))
    print("Connected to Kafka at " + globals.KAFKA_HOSTNAME + ":" + globals.KAFKA_PORT)
    print("Kafka Consumer topic for this Container is " + globals.RECEIVE_TOPIC)
    for message in init.consumer_obj:
        print(message)
        message = message.value
        db_key = str(message)
        db_object = Cache.objects.get(pk=db_key)
        try:
            file_name = db_object.file_name
            print("#############################################")
            print("########## PROCESSING FILE " + file_name)
            print("#############################################")
            print('after redis')
            if db_object.is_doc_type:
                """document"""
                print('in doc type')
                images_array = []
                faces = []
                for cache_obj in db_object.files:
                    pdf_image = str(uuid.uuid4()) + ".jpg"
                    with open(pdf_image, 'wb') as file_to_save:
                        file_to_save.write(cache_obj.file.read())
                    face = recog_face(pdf_image)
                    print("FACE")
                    print(face)
                    if not face:
                        print("NO PERSON RECOGNIZED")
                        continue
                    else:
                        print("PERSON RECOGNIZED: ", face)
                        face_model_object = FaceModel()
                        file_id = cache_obj.file
                        face_model_object.file = file_id
                        face_model_object.document = db_object
                        face_model_object.person = face
                        face_model_object.save()
                        faces.append(face)
                db_object.faces = faces
                db_object.save()
                print(".....................FINISHED PROCESSING FILE.....................")
            else:
                """image"""
                print('in image type')
                file_id = db_object.file
                with open(file_name, 'wb') as file_to_save:
                    file_to_save.write(db_object.file.read())
                face = recog_face(file_name)
                if not face:
                    continue
                else:
                    face_model_object = FaceModel()
                    file_id = db_object.file
                    face_model_object.file = file_id
                    face_model_object.document = db_object
                    face_model_object.person = face
                    face_model_object.save()
                    db_object.faces = [face]
                    face_model_object.save()
                    db_object.save()
                print(".....................FINISHED PROCESSING FILE.....................")
        except Exception as e:
            print(e)
