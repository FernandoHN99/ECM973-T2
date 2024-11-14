import face_recognition
import cv2
import os
import pickle
from datetime import datetime
import numpy as np

def load_known_faces():
    '''Crie aqui a função que carrega as faces conhecidas contidas no arquivo .dat'''

def save_known_faces():
    '''Crie aqui a função que salva as faces conhecidas em um arquivo .dat'''

def register_new_face(face_encoding, face_image, name):
    '''Crie aqui a função registrar novas faces'''

def add_faces_from_gallery(gallery_path):
    '''Crie aqui a função que adiciona as faces contidas em imagens (salvas em uma pasta) no arquivo .dat '''

    ### Carregue o arquivo .dat aqui ! ###

    image_files = ### liste os arquivos da pasta ###
    for image_file in image_files:
        image_path = ### use o os.path.join para escrever o caminho completo ###
        
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processando {image_path}...")

            image = ### Leia a imagem a ser processada ###
            small_frame = ### Diminua na mesma proporção que no código de inferencia ###
            face_locations = ### Gere o BBox da face contida na imagem ###
            face_encodings = ### Gere os encodings da face contida na imagem ###

            for face_encoding in face_encodings:
                name = ### use o os.path.splitext para gerar o nome ###  
                top, right, bottom, left = ### defina com base na localizacao da face ###
                face_image = ### Use o Crop da Face ###
                face_image = ### Faça o resize para (150,150) ###
                ### Registre a nova face aqui ###

    # Salve as faces em um arquivo .dat aqui

if __name__ == "__main__":
    gallery_path = "./gallery"  
    add_faces_from_gallery(gallery_path)
