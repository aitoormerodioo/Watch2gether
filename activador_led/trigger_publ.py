import time
from influxdb_client import InfluxDBClient
import paho.mqtt.client as mqtt

# Configuración de InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "7VQIHFGpHOc2nyXcf3eU28EWPZzOV4SzOce7ZHblLtYhNnx-p37cEeqpfsf4QT57wm8ZSz8P1og84N7RMBF84g=="
influxdb_org = "Deusto"
influxdb_bucket = "sensors_db"

# Configuración del broker MQTT
broker_address = "localhost"  # IP de la Raspberry Pi o broker
mqtt_topic = "raspberry/led"
mqtt_client = mqtt.Client()
mqtt_client.connect(broker_address, 1883, 60)

# Conexión a InfluxDB
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
query_api = influx_client.query_api()

def check_threshold():
    # Consulta para Z (sensor acelerómetro)
    query_z = '''
    from(bucket: "sensors_db")
    |> range(start: -1m)  // Último minuto
    |> filter(fn: (r) => r._measurement == "accelerometer" and r._field == "z")
    |> last()
    '''

    # Verificar Z
    result_z = query_api.query(org=influxdb_org, query=query_z)
    z_critical = False
    for table in result_z:
        for record in table.records:
            z = record.get_value()
            if z > 50:  # Límite para Z
                z_critical = True
                print(f"ALERTA VAS MAS LENTO QUE TU AMIGO")

    # Publicar mensaje MQTT
    if z_critical:
        mqtt_client.publish(mqtt_topic, "ON")  # Enciende el LED
    else:
        mqtt_client.publish(mqtt_topic, "OFF")  # Apaga el LED

try:
    while True:
        check_threshold()
        time.sleep(5)  # Consulta cada 5 segundos

except KeyboardInterrupt:
    print("Interrupción manual. Finalizando...")
    mqtt_client.disconnect()
