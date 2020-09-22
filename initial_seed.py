from db_models.mongo_setup import global_init
from db_models.models.face_model import People
import face_recognition

from pathlib import Path

images_path = list(Path('facedataset').glob('*.*'))

images_name = [ p.stem for p in images_path]

print(images_name, images_path)

global_init()

for idx, image in enumerate(images_path): 
    img = face_recognition.load_image_file(image)
    try:
        face_encoding = face_recognition.face_encodings(img)[0]
        encoding_list = face_encoding.tolist() 
        
        peopleModel = People()
        peopleModel.name = images_name[idx]
        peopleModel.encoding = encoding_list
        peopleModel.save()
    except IndexError:
        print(f"Not able to locate any faces in file {images_name[idx]} Aborting...")
        quit()
