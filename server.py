import socket
import threading

HOST = '127.0.0.1'
PORT = 5000
MAX_HISTORICO = 10


clientes = {}  
historico = []
trava = threading.Lock()

def iniciar_servidor():
    # criando o socket UDP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    
    print(f"[INICIADO] Servidor UDP ouvindo em {HOST}:{PORT}")
    
    try:
        while True:
            # recvfrom retorna os dados e o endereco (ip, porta) de quem enviou.
            dados, endereco = servidor.recvfrom(1024)
            mensagem = dados.decode('utf-8').strip()
            
            if mensagem:
                print(f"[RECEBIDO] de {endereco}: {mensagem}")
                
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor desligado.")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()