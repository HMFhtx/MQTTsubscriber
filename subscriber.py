import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import config

# 1. Setup MongoDB Connection
try:
    mongo_client = MongoClient(config.MONGO_URI)
    db = mongo_client[config.MONGO_DB_NAME]
    collection = db[config.MONGO_COLLECTION_NAME]
    print(f"Connected to MongoDB: {config.MONGO_DB_NAME}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# 2. Define the callback for when a message is received
def on_message(client, userdata, msg):
    try:
        # Decode the payload
        payload_str = msg.payload.decode("utf-8")
        print(f"Received message: {payload_str}")
        
        # Parse JSON data (assuming your MQTT data is JSON)
        data = json.loads(payload_str)

        # 3. Insert into MongoDB
        result = collection.insert_one(data)
        print(f"Saved to MongoDB with ID: {result.inserted_id}")
        
    except json.JSONDecodeError:
        print("Failed to decode JSON. Saving as raw text.")
        collection.insert_one({"raw_payload": payload_str, "topic": msg.topic})
    except Exception as e:
        print(f"Error saving to database: {e}")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.MQTT_TOPIC)

# 4. MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()