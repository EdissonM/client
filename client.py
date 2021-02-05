import pika, os, logging
import datetime
import time
import random
import numpy as np
logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@rabbit/%2f")
params = pika.URLParameters(url)
params.socket_timeout = 5


def envia_mensaje(mensaje):
    connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    channel = connection.channel() # start a channel
    channel.queue_declare(queue="mensajes") # Declare a queue
    channel.basic_publish(exchange="", routing_key="mensajes", body=mensaje)
    connection.close()

for i in range(1000):
    time.sleep(1)
    now = datetime.datetime.now()
    date_string = now.strftime("%d/%m/%y %H:%M:%S")
    data = [i, date_string, "Temperatura", np.random.normal(30, 5, 1)[0]]
    print("Mensaje enviado: " + str(data))
    envia_mensaje("-".join(map(str,data)))
