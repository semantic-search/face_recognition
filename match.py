from db_models.mongo_setup import global_init
import numpy
import face_recognition
from db_models.models.face_model import People

global_init()

matchPath = "facedataset/aron.jpg"
matchImage = face_recognition.load_image_file(matchPath)

try:
    unknown_face_encoding = face_recognition.face_encodings(matchImage)[0]
except IndexError:
    print("Not able to locate any faces. Check the image file. Aborting...")
    quit()

name_list = []
encoding_list = []
for person in People.objects:
    name = person.name
    encoding = person.encoding
    name_list.append(name)
    encoding_list.append(numpy.array(encoding))

results = face_recognition.compare_faces(encoding_list, unknown_face_encoding)
print(name_list)
print(results)

for idx, result in enumerate(results):
    if(result):
        print(f"Match with {name_list[idx]}")
