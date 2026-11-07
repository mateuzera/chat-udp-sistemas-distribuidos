# APS 02 - Servidor de Chat Multiusuário (Sockets UDP) - Equipe 11

Projeto desenvolvido para a disciplina de Redes de Computadores e Sistemas Distribuídos.

## Integrantes
- Igor Soares
- Izadora Taline Gonçalves Andrade
- Mateus Martins
- Mateus Barbosa

## Sumário
- [Descrição do Projeto](#descrição-do-projeto)
- [Funcionalidades Solicitadas](#funcionalidades-solicitadas)
- [Como Executar](#como-executar)

## Descrição do Projeto
O objetivo deste trabalho é implementar um sistema de chat multiusuário em tempo real utilizando Sockets UDP (`SOCK_DGRAM`). O sistema conta com um servidor que gerencia o registro dos clientes ativos pelo seu endereço `(IP, porta)`, retransmite mensagens via broadcast e mantém um buffer de histórico em memória para novos clientes que entram na sala.

## Funcionalidades Solicitadas
- Implementar um servidor de chat multiusuário usando Sockets UDP que permite vários clientes trocando mensagens em uma única sala de chat.
- O servidor deve gerenciar o estado de cada cliente ativo na sessão para retransmitir mensagens em tempo real.
- O cliente entra no chat e define seu nome usando o comando `CONNECT <nome_usuario>`.
- O cliente envia mensagens no chat usando `SEND <mensagem>`.
- O servidor deve retransmitir (broadcast) toda mensagem enviada imediatamente para todos os outros clientes conectados.
- O servidor deve manter um buffer em memória das últimas N mensagens enviadas.
- Quando um novo cliente se registrar, o servidor deve enviar o histórico das últimas N mensagens somente para ele.
- O cliente encerra a sessão através do comando `DISCONNECT`.

## Como Executar

Para abrir o servidor, abra um terminal e utilize o comando:

    python server.py

Para cada cliente, abra um terminal novo e utilize o comando:

    python client.py

No cliente, para entrar no chat e escolher o nome do usuário, utilize:

    CONNECT <nome_usuario>

Para enviar mensagens, no cliente que já está dentro do chat, utilize:

    SEND <mensagem>

Para se desconectar, utilize:

    DISCONNECT