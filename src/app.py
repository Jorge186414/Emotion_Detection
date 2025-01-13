from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import os
from auxiliarFunctions import process_image

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

app.config['PROCESSED_IMAGES_FOLDER'] = processed_images

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

    original_image = request.files['image']

    if original_image.filename == '':
        return jsonify({"error": "El archivo no tiene nombre"}), 400

    # Guardamos la imagen en la carpeta predefinida
    filepath = os.path.join(upload_images_front, original_image.filename)
    original_image.save(filepath)

    result = process_image(filepath)

    # Guardar las imágenes procesadas (sobrescribir siempre las mismas 4)
    processed_images = []
    for idx, img_data in enumerate(result["images"]):
        processed_image_name = f"processed_image_{idx}.jpg"
        processed_image_path = os.path.join(app.config['PROCESSED_IMAGES_FOLDER'], processed_image_name)
        
        # Sobrescribir el archivo procesado
        with open(processed_image_path, "wb") as f:
            f.write(img_data)
        
        processed_images.append(f"./static/images/processed_images/{processed_image_name}")

    return jsonify({"message": "Imágenes procesadas correctamente", "images": processed_images, "emotion": result["emotion"]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)