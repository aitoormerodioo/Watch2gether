import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Configuración del LED
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Configuración del broker MQTT
broker_address = "10.172.117.194"  # IP del ordenador con el script
mqtt_topic = "raspberry/led"

# Función para manejar mensajes MQTT
def on_message(client, userdata, message):
    try:
        msg = message.payload.decode("utf-8")
        print(f"Mensaje recibido: {msg}")
        if msg == "ON":
            GPIO.output(LED_PIN, GPIO.HIGH)  # Enciende el LED
        elif msg == "OFF":
            GPIO.output(LED_PIN, GPIO.LOW)  # Apaga el LED
    except Exception as e:
        print("Error al procesar el mensaje:", e)

# Configuración del cliente MQTT
client = mqtt.Client()
client.connect(broker_address, 1883, 60)
client.subscribe(mqtt_topic)
client.on_message = on_message

# Bucle principal
try:
    print("Escuchando mensajes MQTT...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Interrupción manual. Limpiando GPIO...")
    GPIO.cleanup()
    client.disconnect()
