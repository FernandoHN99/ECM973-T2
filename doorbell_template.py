import face_recognition 
import cv2
from datetime import datetime, timedelta
import numpy as np
import platform
import pickle

known_face_encodings = []
known_face_metadata = []

def warm_up_encoding():
    '''Crie aqui a função que faz a pre inicialização dos modelos'''

    dummy_image =  ### Leia uma imagem dummy que contenha uma face ###
    dummy_locations = ### Gere o BBox da face contida na imagem ###
    if dummy_locations:
        _ = ### Gere os encodings da face contida na imagem ###
    print("Encoding model warmed up.")


def load_known_faces():
    '''Crie aqui a função que carrega as faces conhecidas contidas no arquivo .dat'''


def lookup_known_face(face_encoding):
    '''Crie aqui a função que verifica se a pessoa é conhecida. USE 0.5 como limiar de comparação'''


def main_loop():
    '''Crie a função principal aqui'''


if __name__ == "__main__":
    warm_up_encoding()
    load_known_faces()
    main_loop()
