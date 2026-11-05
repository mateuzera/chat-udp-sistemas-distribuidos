import socket
import threading

HOST = '127.0.0.1'
PORT = 5000
MAX_HISTORICO = 10


clientes = {}  
historico = []
trava = threading.Lock()

def salvar_no_historico(mensagem):
    """Guarda a mensagem e remove a mais antiga se exceder o limite."""
    historico.append(mensagem)
    if len(historico) > MAX_HISTORICO:
        historico.pop(0)

def broadcast(servidor, mensagem, remetente_addr=None):
    """Envia a mensagem para todos os clientes conectados, exceto o remetente."""
    for addr in list(clientes.keys()):
        if addr != remetente_addr:
            try:
                servidor.sendto((mensagem + "\n").encode('utf-8'), addr)
            except Exception as e:
                print(f"[ERRO] Falha ao enviar para {addr}: {e}")

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
            
            if not mensagem:
                continue 

            partes = mensagem.split(" ", 1)
            comando = partes[0].upper()
            argumento = partes[1].strip() if len(partes) > 1 else ""

            with trava:
                if comando == "CONNECT":
                    if endereco not in clientes:
                        clientes[endereco] = argumento
                        servidor.sendto(f"[SERVIDOR] Bem-vindo(a), {argumento}!\n".encode('utf-8'), endereco)
                        
                        # enviando historico pra cliente novo
                        if historico:
                            servidor.sendto(f"--- Histórico das últimas {len(historico)} mensagens ---\n".encode('utf-8'), endereco)
                            for msg in historico:
                                servidor.sendto((msg + "\n").encode('utf-8'), endereco)
                            servidor.sendto("--------------------------------------------\n".encode('utf-8'), endereco)
                        
                        print(f"[REGISTRADO] {endereco} é '{argumento}'")
                        broadcast(servidor, f"[SERVIDOR] {argumento} entrou na sala.", endereco)
                    else:
                        servidor.sendto("[ERRO] Já estás na sala.\n".encode('utf-8'), endereco)

                elif comando == "SEND":
                    if endereco in clientes:
                        nome_usuario = clientes[endereco]
                        msg_formatada = f"[{nome_usuario}]: {argumento}"
                        salvar_no_historico(msg_formatada)
                        print(f"[MENSAGEM] {msg_formatada}")
                        broadcast(servidor, msg_formatada, endereco)
                    else:
                        servidor.sendto("[ERRO] Usa CONNECT <nome> primeiro.\n".encode('utf-8'), endereco)

                elif comando == "DISCONNECT":
                    if endereco in clientes:
                        nome = clientes.pop(endereco)
                        servidor.sendto("[SERVIDOR] Sessão encerrada.\n".encode('utf-8'), endereco)
                        print(f"[DESCONECTADO] {nome} ({endereco}) saiu.")
                        broadcast(servidor, f"[SERVIDOR] {nome} saiu da sala.")
                else:
                    servidor.sendto("[ERRO] Comando inválido.\n".encode('utf-8'), endereco)
                
    except KeyboardInterrupt:
        print("\n[ENCERRANDO] Servidor desligado.")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()