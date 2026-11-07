import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

rodando = True

def receber_mensagens(cliente_socket):
    """Fica escutando as mensagens enviadas pelo servidor UDP em segundo plano."""
    global rodando
    while rodando:
        try:
            dados, _ = cliente_socket.recvfrom(1024)
            mensagem = dados.decode('utf-8')
            if mensagem:
                print(f"\r{mensagem}", end="")
                if rodando:
                    print("> ", end="", flush=True)
        except ConnectionResetError:
            print("\n[ERRO] Servidor indisponível ou porta fechada.")
            rodando = False
            break
        except OSError:
            break

def iniciar_cliente():
    global rodando
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    endereco_servidor = (HOST, PORT)

    print("=== Chat Multiusuário UDP ===")
    print("Comandos: CONNECT <nome> | SEND <mensagem> | DISCONNECT")
    print("-----------------------------\n")

    # Pede o primeiro comando para o sistema operacional alocar a porta UDP local antes da thread ler
    while True:
        primeiro_cmd = input("> ").strip()
        if primeiro_cmd:
            cliente.sendto(primeiro_cmd.encode('utf-8'), endereco_servidor)
            if primeiro_cmd.upper() == "DISCONNECT":
                cliente.close()
                return
            break

    # Inicia a thread para receber o historico e mensagens de outros usuarios em tempo real
    thread_recebimento = threading.Thread(target=receber_mensagens, args=(cliente,), daemon=True)
    thread_recebimento.start()

    try:
        while rodando:
            comando = input("> ").strip()
            if not comando:
                continue

            cliente.sendto(comando.encode('utf-8'), endereco_servidor)

            if comando.upper() == "DISCONNECT":
                rodando = False
                break

    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Saindo do chat...")
        cliente.sendto("DISCONNECT".encode('utf-8'), endereco_servidor)
        rodando = False
    finally:
        cliente.close()

if __name__ == "__main__":
    iniciar_cliente()