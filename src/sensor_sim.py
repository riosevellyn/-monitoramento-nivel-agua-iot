# Simulador de Sensor (Exemplo em Python)
# Envia dados simulados de nível via MQTT

import paho.mqtt.client as mqtt
import time
import random

broker = "localhost"
port = 1883
topic = "/nivel_caixa"

client = mqtt.Client()
client.connect(broker, port)

try:
    while True:
        nivel = random.randint(10, 100)  # Simulação do nível
        client.publish(topic, nivel)
        print(f"Nível enviado: {nivel}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Encerrado pelo usuário.")
    client.disconnect()
