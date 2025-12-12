CONFIG = {
    "device_id": "CDA_02",  
    "room_id": "living_room",
    "broker": "broker.hivemq.com",
    "port": 1883,
    #"username": "sunghyun",
    #"password": "Hivemq2025",
    "topic_prefix": "SensorData",

    # MongoDB Configuration (Fixed syntax)
    "mongo_uri": "mongodb://localhost:27017/",
    "mongo_db_name": "mqtt_data_db",
    "mongo_collection_name": "sensor_readings",
    
    # Sensor configuration
    "read_interval": 10,
    "read_timeout": 3,
    
    # Error handling
    "max_retries": 3,
    "retry_delay": 1
}
