import paho.mqtt.client as mqtt
import json
from influxdb_client import InfluxDBClient
from datetime import datetime

# Configuración del broker MQTT
broker_address = "10.172.117.194"  # Dirección IP del broker SINO localhost
mqtt_topics = ["sensor/heartrate", "sensor/touch", "sensor/accelerometer", "weather"]

# Configuración de InfluxDB
influxdb_url = "http://localhost:8086"  # URL de InfluxDB
influxdb_token = "7VQIHFGpHOc2nyXcf3eU28EWPZzOV4SzOce7ZHblLtYhNnx-p37cEeqpfsf4QT57wm8ZSz8P1og84N7RMBF84g=="       # Genera un token en tu InfluxDB
influxdb_org = "Deusto"       # Organización de InfluxDB
influxdb_bucket = "sensors_db"         # Bucket donde se guardarán los datos

# Conexión al cliente moderno
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influx_client.write_api()

# Función que se ejecuta al recibir un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")  # Decodifica el mensaje
        topic = msg.topic
        
        # Prepara los datos para InfluxDB
        json_body = []
        if topic == "sensor/heartrate":
            json_body = [{
                "measurement": "heartrate",
                "tags": {"sensor": "heart_sensor", "user": payload["user"]},
                "time": datetime.utcnow().isoformat(),
                "fields": {"bpm": payload["bpm"]}  # Ritmo cardíaco en BPM
            }]
        elif topic == "sensor/touch":
            json_body = [{
                "measurement": "touch",
                "tags": {"sensor": "touch_sensor", "user": payload["user"]},
                "time": datetime.utcnow().isoformat(),
                "fields": {"state": payload["state"]}  # Estado táctil: 0 o 1
            }]
        elif topic == "sensor/accelerometer":
            accel_data = json.loads(payload)
            json_body = [{
                "measurement": "accelerometer",
                "tags": {"sensor": "accelerometer", "user": payload["user"]},
                "time": datetime.utcnow().isoformat(),
                "fields": {
                    "x": payload["x"],
                    "y": payload["y"],
                    "z": payload["z"]
                }
            }]
        elif topic == "weather":
            json_body = [{
                "measurement": "weather",
                "tags": {"sensor": "weather_api", "user": payload["user"]},
                "time": datetime.utcnow().isoformat(),
                "fields": {"temperature": payload["temperature"]}
            }]
        
        # Inserta los datos en InfluxDB
        if json_body:
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=json_body)
            print(f"Data written to InfluxDB: {json_body}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Función que se ejecuta al conectar al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    # Suscribirse a todos los topics
    for topic in mqtt_topics:
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, 1883, 60)

# Mantener el cliente en ejecución
try:
    print("Listening for MQTT messages...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Interrupción manual. Cerrando cliente MQTT...")
    client.disconnect()
