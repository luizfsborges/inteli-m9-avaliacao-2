import paho.mqtt.client as mqtt
import time
import random
import json 

# Função para retornar o timestamp
def get_timestamp():
    time_stamp = time.strftime("%d/%m/%Y %H:%M")
    return time_stamp

# Definição do broker
broker = "localhost"
port = 1891

# Definição do cliente
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "python_publisher")

# Conecção ao broker
client.connect(broker, port)

# IDs dos sensores de umidade das estufas agrícolas
sensor_ids = ["gh01h01", "gh01h02", "gh02h01", "gh02h02", "gh01f01", "gh01f02", "gh02f01", "gh02f02"]

# Umidades de teste para os sensores de hortaliças e flores
sensor_test_umidades = [20, 35, 60, 75, 85, 23, 58, 45]

# Modo de publicação de dados
modo_publisher = input("Digite o modo de publicação de dados: [T]este ou [P]rodução: ")

if modo_publisher == "T":
    for i in range(len(sensor_ids)-1):
        sensor_data = {
            "id": sensor_ids[i],
            "tipo": "hortalicas" if i < 4 else "flores",
            "umidade": sensor_test_umidades[i],
            "timestamp": get_timestamp()
        }

        # Publicar dados do sensor no topico "sensor_data" com qos 1
        client.publish("sensor_data", json.dumps(sensor_data))
        print(json.dumps(sensor_data, indent=4))
        time.sleep(1)

elif modo_publisher == "P":
    while True:
        for i in range(len(sensor_ids)-1):
            sensor_data = {
                "id": sensor_ids[i],
                "tipo": "hortalicas" if i < 4 else "flores",
                "umidade": random.randint(20, 90),
                "timestamp": get_timestamp()
            }

            # Publicar dados do sensor no topico "sensor_data" com qos 1
            client.publish("sensor_data", json.dumps(sensor_data))
            print(json.dumps(sensor_data, indent=4))
            time.sleep(1)

client.disconnect()