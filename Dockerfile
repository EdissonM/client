FROM python:3.9

RUN pip install pika
RUN pip install numpy
RUN apt update && apt install tzdata
ENV TZ America/Bogota
COPY . /app
WORKDIR /app
CMD ["python", "client.py"]
