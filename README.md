# Watch2gether

A comprehensive IoT system designed to alleviate loneliness and improve health by enabling physical activities at a distance with a friend or family member. Watch2gether uses a Raspberry Pi with sensors, MQTT communication, and data visualization to connect users in real-time.

## Overview

This project aims to provide an interactive and healthy experience for exercising with a friend or family member, even when both are in different locations. The main functionalities include:

- Monitoring heart rate and physical performance.
- Communicating via double tap to send vibrations to the friend's watch.
- Visual indicators like LEDs to compare performance between users.
- Real-time visualization of the collected data through a web interface.

## System Architecture

The project consists of the following modules:

1. **Raspberry Pi**:
   - Captures sensor data (heart rate, accelerometer, touch).
   - Publishes the data to various topics via MQTT.

2. **MQTT Server**:
   - Receives published data from the Raspberry Pi.
   - Sends the data to an InfluxDB database for storage.

3. **Flask Server**:
   - Provides a web interface to view users' heart rates in real-time.

4. **InfluxDB and Grafana**:
   - InfluxDB stores the data efficiently.
   - Grafana allows advanced and detailed visualization of the collected data.


## Project Features

### Sensors Used
- **Heart Rate Sensor:** Monitors heart rate.
- **Accelerometer:** Determines speed and compares performance.
- **Touch Sensor:** Allows sending tactile notifications.

### Key Functionalities
- Sending and receiving data via the MQTT protocol.
- Managing visual alerts with LEDs based on performance.
- Visualizing historical and real-time data.

## System Requirements

### Hardware
- Raspberry Pi (any model compatible with GPIO).
- Sensors:
  - Heart rate.
  - Accelerometer.
  - Touch sensor.

### Software
- Python 3.x.
- MQTT (Mosquitto).
- InfluxDB.
- Grafana.
- Flask.

### Dependencies
Install the required dependencies with:

```bash
pip install flask paho-mqtt influxdb
```

## Installation Instructions

### Raspberry Pi Configuration
1. Set up the initial Raspberry Pi environment.
2. Install the necessary libraries.
3. Run the following scripts:
   - `sensors_data.py`: Captures sensor data and publishes it to MQTT.
   - `weather_api_data.py`: Fetches weather data and publishes it (uses crontab).
   - `led_sub.py`: Receives data from MQTT and controls a LED based on performance.

### Server Configuration
1. Start the MQTT server:

   ```bash
   mosquitto
   ```

2. Set up InfluxDB to store the data.
3. Run the MQTT server with `servidor.py` to send data to InfluxDB.
4. Access the data through the InfluxDB web interface or Grafana.

### Visualization with Flask
1. Run `app.py` on the Flask server:

   ```bash
   python app.py
   ```

2. Access the web interface in your browser.

## File Structure

- **`raspberry/`**:
  - `sensors_data.py`: Handles sensors and publishes data to MQTT.
  - `weather_api_data.py`: Publishes weather data to MQTT.
  - `led_sub.py`: Controls LEDs based on accelerometer data.

- **`mqttServer/`**:
  - `servidor.py`: Receives MQTT data and saves it to InfluxDB.

- **`flask_server/`**:
  - `app.py`: Flask server for heart rate visualization.
  - `templates/`: Contains the HTML interface.
  - `static/`: Static files (CSS, images).

- **`activator_led/`**:
  - `trigger_publ.py`: Compares speeds and notifies if one user is slower.

## Results

### Screenshots
Include visual examples of:
-Prototype
  ![IMG_1085](https://github.com/user-attachments/assets/7593a585-abd0-49d4-b220-dd7b0ed4b5e1)
- Heart rate data in the Flask interface.
- Detailed graphs in Grafana.


## Credits

- **Group Members:**
  - [Aitor Merodio Benito](https://github.com/aitoormerodioo)
  - [Alejadnro Contreras Alegrua](https://github.com/contreras-alejandro)


---

I hope this README is helpful for documenting your project! If you need adjustments or additional elements, let me know.
