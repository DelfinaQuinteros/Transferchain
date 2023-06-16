# Utilizar una imagen base de Python
FROM python:3.8-slim-buster

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Actualizar pip a la última versión
RUN python -m pip install --upgrade pip

# Instalar las dependencias del sistema
RUN apt-get update && apt-get install -y libffi-dev gcc

# Instalar las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Establecer el comando de inicio de la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
