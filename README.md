# Monitoramento de Nível de Água com IoT e MQTT

Este projeto tem como objetivo monitorar o nível de água de um reservatório utilizando sensores simulados, protocolo MQTT e a plataforma Node-RED.

## Funcionalidades
- Envio de dados do nível de água via MQTT
- Visualização em tempo real no Node-RED
- Acionamento de relé virtual conforme o nível
- Uso de Broker Mosquitto

## Tecnologias Utilizadas
- Wokwi
- MQTT (Broker Mosquitto)
- Simulação de sensores
- Comunicação TCP/IP

## Como Reproduzir
1. Abra o Wokwi e configure o fluxo.
2. Execute o script de simulação do sensor (em `src/`).
3. Configure o broker MQTT no Node-RED.
4. Acompanhe os dados no dashboard do Node-RED.

Veja a [documentação completa](doc/README.md).
