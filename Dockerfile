FROM python:3.10.0-bullseye

RUN apt-get update && apt-get install -y portaudio19-dev

WORKDIR /app

COPY . /app

RUN python ./test.py

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python ./flask_app.py


