import time
from influxdb_client import InfluxDBClient
import RPi.GPIO as GPIO

# Configuración de InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "7VQIHFGpHOc2nyXcf3eU28EWPZzOV4SzOce7ZHblLtYhNnx-p37cEeqpfsf4QT57wm8ZSz8P1og84N7RMBF84g=="
influxdb_org = "Deusto"
influxdb_bucket = "sensors_db"

# Configuración del LED
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

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
                print(f"ALERTA: VAS MAS LENTO QEU TU AMIGO: {z}")

    # Activar o desactivar LED en función de las alertas
    if z_critical:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Enciende el LED
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  # Apaga el LED

try:
    while True:
        check_threshold()
        time.sleep(5)  # Consulta cada 5 segundos

except KeyboardInterrupt:
    print("Interrupción manual. Limpiando GPIO...")
    GPIO.cleanup()
