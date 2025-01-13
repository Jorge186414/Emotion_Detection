from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
import cv2

app = Flask(__name__)
# Permitir todas las solicitudes CORS
CORS(app)

# Rutas para almacenar las imagenes originales y las procesadas
IMAGE_PATH = 'static/images/'

upload_images_front = os.path.join(IMAGE_PATH, 'upload_images')
processed_images = os.path.join(IMAGE_PATH, 'processed_images')

if not os.path.exists(upload_images_front):
    os.makedirs(upload_images_front)

if not os.path.exists(processed_images):
    os.makedirs(processed_images)

# EndPoint para renderizar nuestro Frontend
@app.route('/')
def index():
    return render_template('index.html')

# Funcion y EndPoint para subir imagenes y procesarlas
@app.route('/upload', methods=['POST'])
def upload_images():
    # Verifica si la solicitud contiene un archivo
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró el archivo en la solicitud"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "El archivo no tiene nombre"}), 400

    # Guardamos la imagen en la carpeta predefinida
    filepath = os.path.join(upload_images_front, file.filename)
    file.save(filepath)

    return jsonify({"message": "Archivo guardado exitosamente", "filepath": filepath}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)