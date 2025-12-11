import ssl
import json
from datetime import datetime
import paho.mqtt.client as mqtt
from config import CONFIG

# Config
BROKER = CONFIG["broker"]
PORT = CONFIG["port"]
USERNAME = CONFIG["username"]
PASSWORD = CONFIG["password"]

TOPIC = f'{CONFIG["topic_prefix"]}/{CONFIG["device_id"]}'

#JSON file path
FILE_PATH = "mqtt_messages.json"

#Convert Py obj into JSON. Write recieved message in JSON object
def save_message(obj):
    try:
        with open(FILE_PATH, "a") as f:
            f.write(json.dumps(obj) + "\n")
    except Exception as e:
        print("Error writing to file:", e)

#Connect to broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC}")

#Reciveing message
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received: {payload}")

    message_data = {
        "topic": msg.topic,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat()
    }

    save_message(message_data)


client = mqtt.Client()

# Required for HiveMQ Cloud
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting to broker...")
client.connect(BROKER, PORT, keepalive=60)

client.loop_forever()
