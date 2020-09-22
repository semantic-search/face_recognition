import face_recognition

from pathlib import Path

images_path = list(Path('facedataset').glob('*.*'))

images_name = [ p.stem for p in images_path]

print(images_name, images_path)

for idx, image in enumerate(images_path): 
    img = face_recognition.load_image_file(image)
    try:
        face_encoding = face_recognition.face_encodings(img)[0]
    except IndexError:
        print(f"Not able to locate any faces in file {images_name[idx]} Aborting...")
        quit()
