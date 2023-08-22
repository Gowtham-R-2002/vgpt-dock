FROM python:3.10.0-bullseye

RUN apt-get update && apt-get install -y portaudio19-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN python ./test.py

EXPOSE 8080

CMD python ./flask_app.py


