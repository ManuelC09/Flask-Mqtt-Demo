from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Configuración del broker MQTT
BROKER = "broker.emqx.io"  # Cambia esto al host de tu broker
PORT = 1883
TOPIC = "OxiPulso/Datos"  # Cambia esto al topic que quieras usar

# Variables globales
mqtt_client = mqtt.Client()
messages = []  # Almacena los mensajes recibidos


def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código:", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    global messages
    message = msg.payload.decode()
    print(f"Mensaje recibido: {message}")
    messages.append(message)  # Guarda el mensaje en la lista


# Configurar callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conectar al broker
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()  # Inicia el loop en segundo plano


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    mqtt_client.publish(TOPIC, message)
    return jsonify({"status": "success", "message": "Mensaje enviado"})


@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": messages})


if __name__ == "__main__":
    app.run(debug=True)
