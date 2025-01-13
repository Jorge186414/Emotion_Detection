# Usamos una imagen de Python para el contenedor
FROM python:3.10.16

# Establecemos nuestro directorio de trabajo
WORKDIR /app/src

# Copiamos nuestros archivos al contenedor
COPY . .

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto 5000 para flask
EXPOSE 5000

# Ejecutamos nuestra aplicacion
CMD ["python", "app.py"]
