import paho.mqtt.client as mqtt
import time
import json

# Função para verificar a umidade dos sensores
def verify_umidade(sensor_data):
    if sensor_data["tipo"] == "hortalicas":
        if sensor_data["umidade"] < hortalicas_min_umidade:
            message = {
                "id": sensor_data["id"],
                "tipo": sensor_data["tipo"],
                "umidade": sensor_data["umidade"],
                "timestamp": sensor_data["timestamp"],
                "alerta": "Umidade das hortalicas muito baixa"
            }

            return message
        elif sensor_data["umidade"] > hortalicas_max_umidade:
            message = {
                "id": sensor_data["id"],
                "tipo": sensor_data["tipo"],
                "umidade": sensor_data["umidade"],
                "timestamp": sensor_data["timestamp"],
                "alerta": "Umidade das hortalicas muito alta"
            }

            return message
        else:
            message = {
                "id": sensor_data["id"],
                "tipo": sensor_data["tipo"],
                "umidade": sensor_data["umidade"],
                "timestamp": sensor_data["timestamp"],
                "alerta": "Umidade das hortalicas normal"
            }

            return message
        
    elif sensor_data["tipo"] == "flores":
        if sensor_data["umidade"] < flores_min_umidade:
            message = {
                "id": sensor_data["id"],
                "tipo": sensor_data["tipo"],
                "umidade": sensor_data["umidade"],
                "timestamp": sensor_data["timestamp"],
                "alerta": "Umidade das flores muito baixa"
            }

            return message
        elif sensor_data["umidade"] > flores_max_umidade:
            message = {
                "id": sensor_data["id"],
                "tipo": sensor_data["tipo"],
                "umidade": sensor_data["umidade"],
                "timestamp": sensor_data["timestamp"],
                "alerta": "Umidade das flores muito alta"
            }

            return message
        else:
            message = {
                "id": sensor_data["id"],
                "tipo": sensor_data["tipo"],
                "umidade": sensor_data["umidade"],
                "timestamp": sensor_data["timestamp"],
                "alerta": "Umidade das flores normal"
            }

            return message
        
# Função de callback chamada quando uma mensagem é recebida
def on_message(client, userdata, message):
    sensor_data = json.loads(message.payload)
    message = verify_umidade(sensor_data)
    print(f"Estufa {sensor_data['id'][4]}")
    print(f"{sensor_data['tipo'].capitalize()} {sensor_data['id'][6]}")
    print(f"Umidade: {sensor_data['umidade']}")
    print(f"Status: {message['alerta']}")
    print("\n")

# Definição do broker
broker = "localhost"
port = 1891

hortalicas_min_umidade = 30
hortalicas_max_umidade = 70
flores_min_umidade = 40
flores_max_umidade = 80

# Dfinição do cliente
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "python_subscriber")

client.on_message = on_message

# Conexão ao broker
client.connect(broker, port)

client.subscribe("sensor_data")

# Se a conexão for bem sucedida, exibir mensagem
print("Connected to broker")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Encerrando...")
    client.disconnect()