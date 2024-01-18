FROM python:3.10-slim-bullseye

WORKDIR /var/app

COPY ./static ./static
COPY ./templates ./templates
COPY ./app.py .
COPY ./requirements.txt .

RUN pip3 install -r ./requirements.txt

EXPOSE 7000

CMD ["python3", "app.py"]