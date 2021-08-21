import paho.mqtt.client as mqtt
import time
import pandas as pd
import os

servidor = os.environ.get('SERVER')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(servidor, 1883, 60)
client.loop_start()

df = pd.read_csv ("jena_climate_2009_2016.csv")
for index, row in df.iterrows():
    time.sleep(1)
    client.publish("1/temperatura", "{},temperatura,{},{}".format(row["Date Time"], row['T (degC)'], 'T (degC)'))
    client.publish("1/densidad", "{},densidad,{},{}".format(row["Date Time"], row['rho (g/m**3)'], 'rho (g/m**3)'))

