import os
import face_recognition


def getEncoding(img):
    matchImage = face_recognition.load_image_file(matchPath)
    unknown_face_encoding = face_recognition.face_encodings(matchImage)[0]
    return unknown_face_encoding

def predict(file_name, doc=False):

    try: 
        encoding = getEncoding(file_name)

        results = face_recognition.compare_faces(globals.embeddings, encoding)

        face = [d['name'] for d in results]

        uname = []
        for idx, result in enumerate(results):
            if(result):
                print(f"Match with {face[idx]}")
                uname.append(face[idx])
        
        if doc:
            response = {
                "persons": uname
            }
        else:
            response = {
                "file_name": file_name,
                 "persons": uname,
                "is_doc_type": False
            }

        os.remove(file_name)
        return response
    except IndexError:
        print("Not able to locate any faces. Check the image file.")
        os.remove(file_name)

        return None

   

