import ssl
import paho.mqtt.client as mqtt
from config import CONFIG

#COnfig
BROKER = CONFIG["broker"]
PORT = CONFIG["port"]
USERNAME = CONFIG["username"]
PASSWORD = CONFIG["password"]

TOPIC = f'{CONFIG["topic_prefix"]}/{CONFIG["device_id"]}'


# Connect succces/fail
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"📡 Subscribed to: {TOPIC}")
    else:
        print("Connection failed. Code:", rc)


# Get message, print
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Received on {msg.topic}: {payload}")
    except Exception as e:
        print("Error decoding message:", e)


def main():
    client = mqtt.Client()

    # Set username/password
    client.username_pw_set(USERNAME, PASSWORD)

    # HiveMQ Cloud TLS
    client.tls_set(
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    client.on_connect = on_connect
    client.on_message = on_message

    print("🔌 Connecting...")
    client.connect(BROKER, PORT, keepalive=60)

    client.loop_forever()


if __name__ == "__main__":
    main()
