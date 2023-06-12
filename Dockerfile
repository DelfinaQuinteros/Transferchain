# Utilizar una imagen base de Python
FROM python:3.8

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el resto de los archivos al contenedor
COPY . .

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Establecer el comando de inicio de la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
