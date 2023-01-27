import paho.mqtt.client as mqtt
import time
import pandas as pd
import os

servidor = os.environ.get('SERVER')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + str(msg.payload))

client = mqtt.Client()
client.username_pw_set("guest", password='guest')

client.connect(servidor, 1883, 60)
client.loop_start()

df = pd.read_csv ("jena_climate_2009_2016.csv")
for index, row in df.iterrows():
    time.sleep(1)
    actual_time = time.time_ns()

    client.publish("device_1", 'pepe temperatura={} {}'.format(row['T (degC)'], actual_time))
    client.publish("device_1", 'pepe densidad={} {}'.format(row['rho (g/m**3)'], actual_time))
