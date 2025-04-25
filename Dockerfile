# dockerfiles/dev/django/Dockerfile

FROM python:3.10.2

# ENTRYPOINT ['python', 'instagram/manage.py', 'runserver','0.0.0.0:8000']
# LABEL maintainer="bigdeli.ali3@gmail.com"

# ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD re.txt .

RUN ["pip", "install", "-r", "re.txt"]
# RUN ["python", "manage.py", "makemigrations"]docker-compose up --build
# RUN ["python", "manage.py", "migrate"]

# ADD . .
RUN apt-get update && apt-get install -y netcat
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
# COPY start.sh /start.sh
# RUN chmod +x /start.sh

EXPOSE 8003
