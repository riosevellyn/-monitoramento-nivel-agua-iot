import network
import time
from machine import Pin, I2C
import ujson
from umqtt.simple import MQTTClient

from hcsr04 import HCSR04
from time import sleep
import ssd1306

# MQTT Server Parameters
MQTT_CLIENT_ID = "esp32_hcsr04_01"
MQTT_BROKER    = "test.mosquitto.org"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "sherry/distance"

# ESP32
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=100000)

# Setup I2C for OLED display
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Setup relay pin (Bomba de água)
relay_pin = Pin(19, Pin.OUT)
relay_pin.value(0)  # bomba desligada inicialmente

# Setup botão para ligar/desligar bomba manualmente
button_pin = Pin(23, Pin.IN, Pin.PULL_UP)  # Botão conectado entre pino 23 e GND (ativo baixo)

DISTANCE_THRESHOLD = 10

# Variáveis de controle
pump_state = False          # False = desligado, True = ligado
auto_mode = True            # True = modo automático, False = manual
last_button_state = 1
last_debounce_time = 0
debounce_delay = 50         # ms

oled.fill(0)
oled.show()

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

prev_message = ""

while True:
    distance = sensor.distance_cm()
    # Leitura botão (com debounce simples)
    reading = button_pin.value()
    current_time = time.ticks_ms()

    if reading != last_button_state:
        last_debounce_time = current_time

    if (time.ticks_diff(current_time, last_debounce_time) > debounce_delay):
        # botão está estável, checa se foi pressionado (transição HIGH -> LOW)
        if reading == 0 and last_button_state == 1:
            # botão pressionado, alterna modo manual/auto
            auto_mode = not auto_mode
            print("Modo automático:", auto_mode)

            # Se mudar para modo manual, mantemos o estado atual da bomba
            # Se mudar para modo automático, bomba vai obedecer ao sensor novamente

    last_button_state = reading

    # Controle bomba:
    if auto_mode:
        if distance < DISTANCE_THRESHOLD:
            pump_state = True
        else:
            pump_state = False
    # modo manual: pump_state não muda, fica o que estiver

    relay_pin.value(1 if pump_state else 0)

    # Display OLED
    oled.fill(0)
    oled.text('Distance: {} cm'.format(distance), 0, 0)
    oled.text('Pump: {}'.format("ON" if pump_state else "OFF"), 0, 20)
    oled.text('Mode: {}'.format("Auto" if auto_mode else "Manual"), 0, 40)
    oled.text('Btn toggles mode', 0, 56)
    oled.show()

    # Envia dados MQTT
    data = {
        "distance_cm": distance,
        "pump": "ON" if pump_state else "OFF",
        "mode": "Auto" if auto_mode else "Manual"
    }
    message = ujson.dumps(data)

    if message != prev_message:
        print("Updated! MQTT msg:", message)
        client.publish(MQTT_TOPIC, message)
        prev_message = message
    else:
        print("No change")

    time.sleep(1)
