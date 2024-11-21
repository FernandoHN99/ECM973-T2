from datetime import datetime
import face_recognition
import cv2
import os
import pickle


known_face_encodings = []
known_face_metadata = []

def load_known_faces():
    '''Crie aqui a função que carrega as faces conhecidas contidas no arquivo .dat'''
    if os.path.exists('known_faces.dat'):
        with open('known_faces.dat', 'rb') as f:
            known_faces = pickle.load(f)
    else:
        known_faces = []
    return known_faces

def save_known_faces():
    '''Crie aqui a função que salva as faces conhecidas em um arquivo .dat'''
    with open("known_faces.dat", "wb") as face_data_file:
        face_data = [known_face_encodings, known_face_metadata]
        pickle.dump(face_data, face_data_file)
        print("Known faces backed up to disk.")

def register_new_face(face_encoding, face_image, name):
    '''Crie aqui a função registrar novas faces'''
    known_face_encodings.append(face_encoding)
    known_face_metadata.append({
    "first_seen": datetime.now(),
    "first_seen_this_interaction": datetime.now(),
    "last_seen": datetime.now(),
    "seen_count": 1,
    "seen_frames": 1,
    "face_image": face_image,
    "name": name,
    })


def add_faces_from_gallery(photos_path):
    '''Crie aqui a função que adiciona as faces contidas em imagens (salvas em uma pasta) no arquivo .dat '''

    known_faces = load_known_faces()

    image_files = os.listdir(photos_path)
    for image_file in image_files:
        image_path = os.path.join(photos_path, image_file)
        
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processando {image_path}...")

            image = cv2.imread(image_path)
            small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

            face_locations = face_recognition.face_locations(small_frame)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations)

            for face_encoding in face_encodings:
                name = os.path.splitext(image_file)[0]
                top, right, bottom, left = face_locations[0]
                face_image = image[top*4:bottom*4, left*4:right*4]
                face_image = cv2.resize(face_image, (150, 150))
                register_new_face(face_encoding, face_image, name)

    save_known_faces()

if __name__ == "__main__":
    photos_path = "./photos"  
    add_faces_from_gallery(photos_path)