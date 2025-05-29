from flask import Flask, request, render_template_string, jsonify
from flask_socketio import SocketIO
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

NODE_NAME = os.environ.get("NODE_NAME", "nodo1")
NEXT_NODE = os.environ.get("NEXT_NODE") 
INCREMENT = int(os.environ.get("INCREMENT", 1))

current_value = 0
history = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ node_name }}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            var socket = io();

            socket.on('update', data => {
                document.getElementById('valor').textContent = data.value;
                let historial = document.getElementById('historial');
                historial.innerHTML = '';
                data.history.forEach(val => {
                    let li = document.createElement('li');
                    li.textContent = val;
                    historial.appendChild(li);
                });
            });
        });
    </script>
</head>
<body>
    <h1>Soy {{ node_name }}</h1>
    <p>Valor actual: <strong id="valor">{{ value }}</strong></p>
    {% if is_first_node %}
        <form method="post" action="/iniciar">
            <button type="submit">Iniciar flujo</button>
        </form>
    {% endif %}
    <h3>Historial:</h3>
    <ul id="historial">
    {% for val in history %}
        <li>{{ val }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/', methods=["GET"])
def home():
    return render_template_string(
        HTML_TEMPLATE,
        node_name=NODE_NAME,
        value=current_value,
        is_first_node=(NODE_NAME == "nodo1"),
        history=reversed(history)
    )

@app.route('/iniciar', methods=["POST"])
def iniciar():
    global current_value
    value = current_value
    return process_value(value)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    value = data.get("value", 0)
    return process_value(value)

def process_value(value):
    global current_value
    value += INCREMENT
    current_value = value
    history.append(value)
    print(f"[{NODE_NAME}] Valor actualizado a {value}")

    socketio.emit('update', {'value': current_value, 'history': list(reversed(history))})

    if NEXT_NODE:
        try:
            requests.post(f"{NEXT_NODE}/process", json={"value": value})
        except Exception as e:
            print(f"[{NODE_NAME}] Error enviando a siguiente nodo: {e}")
    else:
        try:
            requests.post("http://nodo1:5000/reset", json={"value": value})
        except Exception as e:
            print(f"[{NODE_NAME}] Error enviando reset a nodo1: {e}")

    return '', 204

@app.route('/reset', methods=['POST'])
def reset():
    global current_value
    data = request.get_json()
    value = data.get("value", 0)
    current_value = value
    history.append(value)
    print(f"[{NODE_NAME}] Reiniciando ciclo con valor: {value}")
    socketio.emit('update', {'value': current_value, 'history': list(reversed(history))})
    return '', 204

if __name__ == '__main__':

    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host="0.0.0.0", port=5000)
