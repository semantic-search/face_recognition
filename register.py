from fastapi import FastAPI, File, UploadFile, Form
from db_models.mongo_setup import global_init
from db_models.models.user_model import UserModel
import face_recognition
import pickle
import os
import globals


app = FastAPI()
global_init()

for user in UserModel.objects:
    globals.add_to_embeddings(username=user.user_name, encoding=pickle.loads(user.encoding))


@app.post("/register/")
def register(
        file: UploadFile = File(...),
        user_name: str = Form(...),
        full_name: str = Form(...)
):
    try:
        UserModel.objects.get(user_name=user_name)
        return False
    except UserModel.DoesNotExist:
        user_model_obj = UserModel()
        file_name = file.filename
        with open(file_name, 'wb') as f:
            f.write(file.file.read())
        face_image = face_recognition.load_image_file(file_name)
        face_encoding = face_recognition.face_encodings(face_image)[0]
        binary_encoding = pickle.dumps(face_encoding)
        user_model_obj.user_name = user_name
        user_model_obj.full_name = full_name
        user_model_obj.encoding = binary_encoding
        with open(file_name, 'rb') as fd:
            user_model_obj.img.put(fd)
        os.remove(file_name)
        user_model_obj.save()
        return True
