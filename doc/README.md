# Documentação Técnica

## Hardware Utilizado (Simulado)
- Sensor ultrassônico (simulado via software)
- Relé virtual
- Conexão via rede local TCP/IP

## Comunicação
- Protocolo MQTT com tópicos:
  - `/nivel_caixa` para dados do sensor
  - `/comando_rele` para atuação

- Broker MQTT: Mosquitto

## Arquitetura
O projeto utiliza a arquitetura pub/sub do MQTT para comunicação entre os dispositivos simulados.

Veja os diagramas na pasta `img/`.
