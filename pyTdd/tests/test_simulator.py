import unittest
import paho.mqtt.client as mqtt
import time
import json

# Configuração dos parâmetros MQTT
broker = 'localhost'
port = 1891
topic = "sensor_data"
client_id_publisher = 'python_publisher_test'
client_id_subscriber = 'python_subscriber_test'

# Variável global para armazenar mensagens recebidas para validação
received_messages = []

class TestIoTSimulator(unittest.TestCase):
    def setUp(self):
        # Configuração do cliente para publicação
        self.publisher_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=client_id_publisher, clean_session=True, protocol=mqtt.MQTTv311)
        self.publisher_client.connect(broker, port)

        # Configuração do cliente para subscrição
        self.subscriber_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=client_id_subscriber, clean_session=True, protocol=mqtt.MQTTv311)
        self.subscriber_client.on_message = self.on_message
        self.subscriber_client.connect(broker, port)
        self.subscriber_client.subscribe(topic)
        self.subscriber_client.loop_start()
        time.sleep(1)  # Garante que o subscriber seja configurado antes dos testes

    def tearDown(self):
        # Desconecta os clientes MQTT após os testes
        self.subscriber_client.loop_stop()
        self.subscriber_client.disconnect()
        self.publisher_client.disconnect()

    def on_message(self, client, userdata, message):
        # Função callback para mensagens recebidas
        received_messages.append(message.payload.decode())
        print(f"Received message in test subscriber: {message.payload.decode()}")

    def test_data_reception(self):
        """Testa se os dados são recebidos corretamente pelo broker MQTT."""
        test_message = {
            "id": "gh01h01",
            "tipo": "hortalicas",
            "umidade": 20,
            "timestamp": "22/09/2021 14:00"
        }
        self.publisher_client.publish(topic, json.dumps(test_message))
        time.sleep(2)  # Aguarda 2 segundos para a mensagem ser recebida
        self.assertIn(json.dumps(test_message), received_messages, "A mensagem de teste não foi recebida.")

    def test_data_validation(self):
        """Testa se os dados recebidos correspondem aos dados enviados."""
        # Supõe que test_data_reception já adicionou uma mensagem a received_messages
        test_message = {
            "id": "gh01h01",
            "tipo": "hortalicas",
            "umidade": 20,
            "timestamp": "22/09/2021 14:00"
        }
        self.assertEqual(received_messages[-1], json.dumps(test_message), "A mensagem recebida não corresponde à mensagem enviada.")

if __name__ == '__main__':
    unittest.main()


