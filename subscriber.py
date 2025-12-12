import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import config
import ssl # Needed for HiveMQ Cloud connection

# Create a shortcut to the configuration dictionary
conf = config.CONFIG

# 1. Setup MongoDB Connection
try:
    # Accessing config via dictionary keys
    mongo_client = MongoClient(conf["mongo_uri"])
    db = mongo_client[conf["mongo_db_name"]]
    collection = db[conf["mongo_collection_name"]]
    print(f"Connected to MongoDB: {conf['mongo_db_name']}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# 2. Define the callback for when a message is received
def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8")
        print(f"Received message on {msg.topic}: {payload_str}")
        
        # Parse JSON data
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
    if rc == 0:
        print("Connected successfully!")
        # Subscribe to all topics starting with the prefix
        topic = f"{conf['topic_prefix']}/#"
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    else:
        print(f"Connection failed with result code {rc}")

# 4. MQTT Client Setup
client = mqtt.Client()

# --- VITAL FIXES FOR HIVEMQ CLOUD ---
# Set username and password
#client.username_pw_set(conf["username"], conf["password"])

# Enable SSL/TLS (Required for port 8883)
# ------------------------------------

client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to broker {conf['broker']}...")
client.connect(conf["broker"], conf["port"], 60)

client.loop_forever()
