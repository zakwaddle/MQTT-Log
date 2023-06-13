from paho.mqtt import client as mqtt_client
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv('API_URL')
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = os.getenv('MQTT_PORT')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PW = os.getenv('MQTT_PW')
LOG_TOPIC = os.getenv('LOG_TOPIC')


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(LOG_TOPIC)
        print(f"Listening to topic: {LOG_TOPIC}\n")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    try:
        log_msg = json.loads(msg.payload)

        log = {"log": log_msg, "topic": msg.topic}
        print(log)
        r = requests.post(API_URL, json=log)
        print(r.status_code)

        # Send a confirmation of receipt message to the topic specified in the received message
        # client.publish(msg.payload.decode(), "Confirmation of receipt")
    except json.JSONDecodeError:
        print("not json: ", msg)


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=MQTT_USER, password=MQTT_PW)
    client.connect(host=MQTT_HOST, port=int(MQTT_PORT))
    return client


if __name__ == "__main__":
    mqtt_listener = connect_mqtt()
    try:
        mqtt_listener.loop_forever()
    except Exception as e:
        print(e)
    finally:
        mqtt_listener.loop_stop()
