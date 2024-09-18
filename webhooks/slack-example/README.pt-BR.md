# Slack

Neste exemplo, recebemos notificações de novos agendamentos via webhook e enviamos um alerta para um canal do Slack, utilizando o AWS API Gateway e o AWS Lambda para executar código serverless de forma eficiente. Essa configuração garante escalabilidade e processamento de baixa latência, tornando-a ideal para notificações em tempo real em ambientes de nuvem.

## Configuração

- Variável de ambiente: `SLACK_TOKEN` - Token de autenticação para o Slack.

## Como Utilizar

O código está pré-configurado para ser executado como uma função AWS Lambda. Para começar, faça o deploy do código em seu ambiente AWS. Certifique-se de configurar o endpoint da AWS nas configurações de webhook da eAgenda para apontar para o endpoint do AWS API Gateway. Essa configuração permitirá que sua função Lambda receba e processe notificações de webhook da eAgenda de maneira eficiente.