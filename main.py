from typing_extensions import final
from db_models.models.user_model import UserModel
from db_models.models.cache_model import Cache
import json
import uuid
from db_models.mongo_setup import global_init
import init
import globals
import pickle
import atexit
from face_service import predict

for user in UserModel.objects:
    globals.add_to_embeddings(username=user.user_name, encoding=pickle.loads(user.encoding))


def send_to_topic(topic, value_to_send_dic):
    data_json = json.dumps(value_to_send_dic)
    init.producer_obj.send(topic, value=data_json)


if __name__ == "__main__":
    global_init()
    print('main fxn')

    try:
        init.redis_obj.set(globals.RECEIVE_TOPIC, globals.CONNECTED)

        for message in init.consumer_obj:
            print(message)
            message = message.value
            db_key = str(message)  

            db_object = Cache.objects.get(pk=db_key)
            file_name = db_object.file_name
            init.redis_obj.set(globals.RECEIVE_TOPIC, file_name)
            print('after redis')
            if db_object.is_doc_type:
                """document"""
                print('in doc type')
                images_array = []
                for image in db_object.files:
                    pdf_image = str(uuid.uuid4()) + ".jpg"
                    with open(pdf_image, 'wb') as file_to_save:
                        file_to_save.write(image.file.read())
                    images_array.append(pdf_image)
                persons_list = []
                coords_list = []
                text_predictions = []
                for image in images_array:
                    image_results = predict(image, doc=True)
                    
                    if image_results == None :
                        continue

                    persons = image_results["persons"]
                    persons_list.append(persons)

                res = {
                    "container_name": globals.RECEIVE_TOPIC,
                    "file_name": file_name,
                    "persons": persons_list,
                    "is_doc_type": True
                }
               
                print(res, "full_res")
                send_to_topic(globals.SEND_TOPIC_FULL, value_to_send_dic=res)
                send_to_topic(globals.SEND_TOPIC_TEXT, value_to_send_dic=res)
                init.producer_obj.flush()
            else:
                """image"""
                print('in image type')
                if db_object.mime_type in globals.ALLOWED_IMAGE_TYPES:
                    with open(file_name, 'wb') as file_to_save:
                        file_to_save.write(db_object.file.read())
                    full_res = predict(file_name)

                    if full_res == None :
                        continue
                    
                    print(f"full_res {full_res}")

                    full_res["container_name"] = globals.RECEIVE_TOPIC
                    
                    print(full_res, 'full_res')
                    send_to_topic(globals.SEND_TOPIC_FULL, value_to_send_dic=full_res)
                    send_to_topic(globals.SEND_TOPIC_TEXT, value_to_send_dic=full_res)
                    init.producer_obj.flush()

def exit_handler():
    init.redis_obj.set(globals.RECEIVE_TOPIC, globals.DISCONNECTED)

atexit.register(exit_handler)
