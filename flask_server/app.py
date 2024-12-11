from flask import Flask, render_template
from influxdb_client import InfluxDBClient

app = Flask(__name__)

# Configuración de InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "7VQIHFGpHOc2nyXcf3eU28EWPZzOV4SzOce7ZHblLtYhNnx-p37cEeqpfsf4QT57wm8ZSz8P1og84N7RMBF84g=="
influxdb_org = "Deusto"
influxdb_bucket = "sensors_db"
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
query_api = influx_client.query_api()

@app.route('/')
def index():
    # Consulta para obtener datos del sensor de heartrate
    query = '''
    from(bucket: "sensors_db")
    |> range(start: -24h)
    |> filter(fn: (r) => r._measurement == "heartrate" and r._field == "bpm")
    |> sort(columns: ["_time"], desc: true)
    '''
    result = query_api.query(org=influxdb_org, query=query)
    data = [{"time": record.get_time(), "bpm": record.get_value()} for table in result for record in table.records]

    # Consulta para obtener el último usuario registrado
    user_query = '''
    from(bucket: "sensors_db")
    |> range(start: -24h)
    |> filter(fn: (r) => r._measurement == "heartrate")
    |> keep(columns: ["user", "_time"])
    |> sort(columns: ["_time"], desc: true)
    |> limit(n: 1)
    '''
    user_result = query_api.query(org=influxdb_org, query=user_query)
    user = next((record.values["user"] for table in user_result for record in table.records), "Usuario")

    return render_template("index.html", data=data, user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
