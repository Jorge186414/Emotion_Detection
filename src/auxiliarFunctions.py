import cv2
import mediapipe as mp
from PIL import Image, ImageEnhance
import numpy as np
import os
from deepface import DeepFace

# Inicializamos el modelo de detección de rostros de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

def process_image(image_path):
    # Aplicamos las transformaciones a nuestra imagen
    image, gray_image, gray_image_bgr = transform_image(image_path)

    # Detectar los puntos faciales y dibujar las X
    points = detect_key_facials(gray_image, gray_image_bgr)
    
    # Almacenar imagenes con transformaciones
    images = []
    # Imagen original con puntos faciales
    images.append(gray_image_bgr)
    # Imagen girada 180 grados
    rotated = cv2.rotate(gray_image_bgr, cv2.ROTATE_180)
    images.append(rotated)
    # Imagen volteada horizontalmente (espejo)
    flipped = cv2.flip(gray_image_bgr, 1)
    images.append(flipped)
    # Imagen con brillo ajustado
    brightened = adjust_brightness(gray_image_bgr, 1.5)  # Incrementa el brillo en un 50%
    images.append(brightened)
    # Imagen alineada
    aligned = cv2.warpAffine(gray_image_bgr, cv2.getRotationMatrix2D((gray_image_bgr.shape[1] / 2, gray_image_bgr.shape[0] / 2), 0, 1), (gray_image_bgr.shape[1], gray_image_bgr.shape[0]))
    images.append(aligned)

    # Detectar la emoción de la imagen
    emotion = detect_emotion(image)
    
    # Guardamos las imágenes generadas en un buffer de memoria y devolverlas como bytes
    processed_images = [] 
    for idx, img in enumerate(images):
        img_byte_arr = image_to_bytes(img)
        processed_images.append(img_byte_arr)
    
    return {"message": "Imagen procesada", "images": processed_images, "emotion": emotion}

def detect_emotion(image):
    analysis = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
    return analysis[0]['dominant_emotion']

def transform_image(image_path):
    # Leer la imagen
    image = cv2.imread(image_path)

    # Convertir a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convertir la imagen en escala de grises a BGR para poder dibujar en color
    gray_image_bgr = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

    return image, gray_image, gray_image_bgr

def detect_key_facials(gray_image, output_image):
    results = face_mesh.process(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB))
    points = []
    
    eye_indices = [33, 133, 362, 263]  # Ojos: arriba, abajo, izquierda, derecha
    eyebrow_indices = [70, 107, 336, 296]  # Cejas: izquierda y derecha de cada ceja
    nose_indices = [1, 197, 5]  # Nariz: centro, izquierda, derecha
    lips_indices = [13, 14, 78, 308]  # Labios: arriba, abajo, izquierda, derecha
    
    relevant_indices = eye_indices + eyebrow_indices + nose_indices + lips_indices
    
    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            for idx, landmark in enumerate(landmarks.landmark):
                if idx in relevant_indices:  
                    x = int(landmark.x * gray_image.shape[1])
                    y = int(landmark.y * gray_image.shape[0])
                    points.append((x, y))
                    size = max(3, int(gray_image.shape[1] * 0.01))  
                    color = (0, 0, 255)  
                    thickness = 1  
                    cv2.line(output_image, (x - size, y - size), (x + size, y + size), color, thickness)
                    cv2.line(output_image, (x - size, y + size), (x + size, y - size), color, thickness)
    
    return points

def adjust_brightness(image, factor):
    pil_image = Image.fromarray(image)
    enhancer = ImageEnhance.Brightness(pil_image)
    bright_image = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(bright_image), cv2.COLOR_RGB2BGR)

def image_to_bytes(image):
    is_success, img_encoded = cv2.imencode('.jpg', image)  
    if is_success:
        return img_encoded.tobytes() 
    else:
        return None

