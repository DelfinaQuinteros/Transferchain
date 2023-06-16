# Utilizar una imagen base de Python
FROM python:3.8-alpine3.15

# Establecer el directorio de trabajo en /app
WORKDIR /app

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r requirements.txt

#Instala dependencias del sistema
RUN apk add mariadb-dev py3-mysqlclient mysql-client
# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Establecer el comando de inicio de la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
