# Utilizar una imagen base de Python
FROM python:3.8-alpine3.15

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos al contenedor
COPY . .

#Instala dependencias del sistema
RUN apk add mariadb-dev py3-mysqlclient mysql-client
# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Establecer el comando de inicio de la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
