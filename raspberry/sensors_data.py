import paho.mqtt.client as mqtt
import random
import time
import json
import max30100
import os
import RPi.GPIO as GPIO
from datetime import datetime
from smbus import SMBus

# Configuración del broker MQTT
broker_address = "10.172.117.194"  # Cambia esto por la IP de tu portátil
client = mqtt.Client()
client.connect(broker_address, 1883, 60)

# Topics para cada sensor
topic_hr = "sensor/heartrate"
topic_touch = "sensor/touch"
topic_accel = "sensor/accelerometer"

# Inicialización del sensor MAX30100 - HEART SENSOR ________
mx30 = max30100.MAX30100()
mx30.enable_spo2()

# Configura el modo de numeración de pines (BCM o BOARD) TOUCH SENSOR_________
GPIO.setmode(GPIO.BCM)
# Configura el pin al que está conectado el sensor táctil (cambia el número de pin si es necesario)
touch_pin = 16  ## Ponerlo en el D16
# Configura el pin como entrada
GPIO.setup(touch_pin, GPIO.IN)

# Configurar el address del Accel 3 ejes - ACCELEROMETER_____________
i2cbus = SMBus(1)  # Create a new I2C bus
i2caddress = 0x4C  # Address of MCP23017 device (IZQUIER I2C)
i2cbus.write_byte_data(i2caddress, 0x07, 0x01) # ON mode

log_file = "/home/pi/Desktop/ejercicios/proyecto/log_local/sensors_log.txt"

user_id = "raspberry_01"

# Función para escribir en el archivo de log
def write_log(data):
    with open(log_file, "a") as file:
        file.write(data + "\n")

# Función para obtener el ritmo cardíaco
def get_heart_rate():
    try:
        mx30.read_sensor()  # Lee el sensor

        # Calcular el ritmo cardíaco en BPM
        hb = int(mx30.ir / 100)
        spo2 = int(mx30.red / 100)
        
        if mx30.ir != mx30.buffer_ir:
            return {"user": user_id, "bpm": hb}
        else:
            return None  # En caso de no detectar cambio en IR, devuelve None
            
    except Exception as e:
        print("Error al obtener el ritmo cardíaco:", e)
        return None


# Función para obtener el estado de touch
def get_touch():
    try:
        if GPIO.input(touch_pin):
            return {"user": user_id, "state": 1}
        else:
            return {"user": user_id, "state": 0}
    except Exception as e:
        print("Error al obtener el valor de touch:", e)
        return None

# Función para obtener los datos del acelerómetro
def get_accelerometer():
    try:
        X = i2cbus.read_byte_data(i2caddress, 0x00)  # Read the value of Port B
        Y = i2cbus.read_byte_data(i2caddress, 0x01)  # Read the value of Port B
        Z = i2cbus.read_byte_data(i2caddress, 0x02)  # Read the value of Port B
        return { "user": user_id,
            "x": X ,
            "y": Y ,
            "z": Z 
        }
    except Exception as e:
        print("Error al obtener datos del acelerómetro:", e)
        return None

try:
    # Bucle infinito para enviardatos de sensores cada segundo
    while True:
        
        log_data = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        accelerometer = get_accelerometer()
        if accelerometer is not None:
            client.publish(topic_accel, json.dumps(accelerometer))  # Envía como JSON
            log_data["accelerometer"] = accelerometer

        # Obtiene y publica datos de cada sensor individualmente con manejo de errores
        heart_rate = get_heart_rate()
        if heart_rate is not None:
            client.publish(topic_hr, json.dumps(heart_rate)) #en BPM
            heart_value = heart_rate["bpm"]
            log_data["heart_rate"] = heart_value

        touch = get_touch()
        if touch is not None:
            client.publish(topic_touch, json.dumps(touch))
            touch_value = touch["state"]
            log_data["touch"] = touch_value

        
        write_log(json.dumps(log_data))
        # Espera 1 segundo antes de la siguiente iteración
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupción manual. Desconectando...")
    GPIO.cleanup()
    client.disconnect()
