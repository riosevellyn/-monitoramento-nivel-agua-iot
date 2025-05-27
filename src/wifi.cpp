#include <WiFi.h>
#include <PubSubClient.h>

// Configurações de Wi-Fi (WokWi simula isso)
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Configurações do MQTT
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_topic = "/nivel_caixa";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
int value = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando-se ao WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop até que esteja conectado
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("conectado");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    int nivelAgua = random(20, 100); // Simula um nível aleatório da água
    char msg[50];
    snprintf(msg, 50, "Nivel da caixa: %d cm", nivelAgua);
    Serial.print("Publicando mensagem: ");
    Serial.println(msg);
    client.publish(mqtt_topic, msg);
  }
}
