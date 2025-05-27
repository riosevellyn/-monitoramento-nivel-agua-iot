# Documentação Técnica

## Hardware Utilizado (Simulado)
- Sensor Ultrassônico (HC-SR04) – simulado via software no WokWi

- Relé Virtual (5V) – usado para simular acionamento da bomba

- Microcontrolador Arduino Uno – unidade de controle central

- Conexão de rede via TCP/IP local – para comunicação entre os dispositivos e o broker

## Comunicação
- Protocolo Utilizado: MQTT (Message Queuing Telemetry Transport)

- Broker: Mosquitto (executado localmente na simulação)

## Tópicos MQTT utilizados:
- /nivel_caixa → Envia os dados simulados do nível da caixa d’água

- /comando_rele → Recebe os comandos de controle da bomba (liga/desliga)

## Arquitetura
O sistema foi desenvolvido com base na arquitetura pub/sub do protocolo MQTT, com os seguintes elementos:

- Elemento	Função
- Sensor	Publicador de dados no tópico /nivel_caixa
- Relé	Assinante que atua conforme os dados recebidos
- Broker	Intermediário que roteia as mensagens entre sensor e relé
- WokWi	Plataforma de simulação que integra os dispositivos e gerencia lógica

## Demonstração da Comunicação MQTT
Durante a execução do sistema:

- O sensor publica um valor de nível simulado em /nivel_caixa

- O relé recebe esse valor via MQTT e decide se ativa ou desativa a bomba

- Para visualização, pode-se usar:

- MQTT Explorer

- Terminal com Mosquitto


