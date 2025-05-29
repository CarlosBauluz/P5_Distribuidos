from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

NODE_NAME = os.environ.get("NODE_NAME", "nodo1")
NEXT_NODE = os.environ.get("NEXT_NODE")
INCREMENT = int(os.environ.get("INCREMENT", 1))

# Estado interno
current_value = 0
history = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ node_name }}</title>
</head>
<body>
    <h1>Soy {{ node_name }}</h1>
    <p>Valor actual: <strong>{{ value }}</strong></p>
    {% if is_first_node %}
        <form method="post" action="/iniciar">
            <button type="submit">Iniciar flujo</button>
        </form>
    {% endif %}
    <h3>Historial:</h3>
    <ul>
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

    try:
        response = app.test_client().post('/process', json={"value": value})
        if response.status_code == 204:
            return '', 204
        else:
            return jsonify({"error": "Error iniciando flujo"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST'])
def process():
    global current_value
    data = request.get_json()
    value = data.get("value", 0)
    source = data.get("source", None)

    value += INCREMENT
    current_value = value
    history.append(value)

    print(f"[{NODE_NAME}] Recibido: {data.get('value')} → +{INCREMENT} = {value}")

    if NEXT_NODE:
        try:
            response = requests.post(
                f"{NEXT_NODE}/process", 
                json={"value": value, "source": source or NODE_NAME}
            )
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        try:
            print(f"[{NODE_NAME}] Enviando resultado final {value} de vuelta a nodo1")
            response = requests.post("http://nodo1:5000/reset", json={"value": value})
            return '', 204
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset():
    global current_value
    data = request.get_json()
    value = data.get("value", 0)

    print(f"[{NODE_NAME}] Reiniciando ciclo con valor: {value}")
    current_value = value
    history.append(value)

    return '', 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
