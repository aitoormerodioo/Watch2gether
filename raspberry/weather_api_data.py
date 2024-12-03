import paho.mqtt.client as mqtt
import requests
import json
import time
import os
from datetime import datetime

# Configuración del broker MQTT
broker_address = "10.172.117.194"  # Cambia esto por la IP de tu portátil
client = mqtt.Client()
client.connect(broker_address, 1883,60)

client.loop_start()
# Topic para la temperatura de Bilbao
topic_weather = "weather"

log_file = "/home/pi/Desktop/ejercicios/proyecto/log_local/weather_log.txt"

# Función para obtener la temperatura de Bilbao
def get_bilbao_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 43.263,
            "longitude": -2.935,
            "current_weather": "true"
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data["current_weather"]["temperature"]
            return temperature
        else:
            print("Error al obtener datos del tiempo en Bilbao:", response.status_code)
            return None
    except Exception as e:
        print("Error al realizar la solicitud HTTP:", e)
        return None

# Función para escribir en el archivo de log
def write_log(data):
    with open(log_file, "a") as file:
        file.write(data + "\n")
        
# Obtiene y publica la temperatura de Bilbao
temperature_bilbao = get_bilbao_weather()
if temperature_bilbao is not None:
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Temperature in Bilbao {temperature_bilbao} ºC"
    client.publish(topic_weather, str(temperature_bilbao))
    print(f"Temperature in Bilbao: {temperature_bilbao} °C")
    write_log(log_entry)
    time.sleep(1)
    
client.loop_stop()
client.disconnect()