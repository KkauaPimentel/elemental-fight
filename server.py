import socket
import pickle
import threading

'''
Cada jogador é representado por uma tupla: (objt, flag)
ambos estão como (None, False) no começo
Por enquanto só suporta 2 primeiros players
'''
state1 = (None, False)  # Para o jogador 1 (cliente 1)
state2 = (None, False)  # Para o jogador 2 (cliente 2)

'''
Fiz uso do lock para garantir que não haja conflito entre as interações.
Ele sincroniza as movimentações/mudanças nos estados.
''' 
lock = threading.Lock()

def handle_client(conn, player):
    global state1, state2

    while True:
        try:
            
            data_bytes = conn.recv(4096)
            if not data_bytes:
                break
            # Desserializa a mensagem(É uma tupla)
            msg = pickle.loads(data_bytes)
            with lock:
                # Controle de interações
                if player == 1:
                    state1 = msg
                else:
                    state2 = msg
                # Envia para cada cliente o estado do oponente
                if player == 1:
                    op_state = state2
                else:
                    op_state = state1

            conn.sendall(pickle.dumps(op_state))
        except Exception as e:
            print(f"Erro no handle_client (player {player}):", e)
            break
    # Se sair do ciclo, encerra a conexão
    conn.close()
    print(f"Cliente {player} desconectado.")

def udp_discovery():
    """
    Serviço UDP para descoberta automática do servidor.
    Escuta na porta 9000 por mensagens 'cade_server' e responde com 'aqui_estou'.
    """

    # Endereço global, onde aceita conexões de onde for
    UDP_IP = "0.0.0.0"
    UDP_PORT = 9000
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_IP, UDP_PORT))
    print("Serviço UDP de descoberta iniciado na porta", UDP_PORT)
    while True:
        try:
            #addr é o adress do cliente que quer conectar
            data, addr = udp_sock.recvfrom(1024)
            if data.decode().strip() == "cade_server":
                # Permite a conexão do endereço recebido
                udp_sock.sendto("aqui_estou".encode(), addr)
        except Exception as e:
            print("Erro no serviço UDP:", e)

def main():
    # Inicia a thread de descoberta UDP
    # Usa a thread para manter o fluxo sem ter a necessidade de interromper a main
    # A conexão usada a partir daqui é TCP
    threading.Thread(target=udp_discovery, daemon=True).start()
    
    server_ip = "0.0.0.0"
    server_port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, server_port))
    s.listen(6)
    print(f"Servidor iniciado em {server_ip}:{server_port}")
    
    clients = []
    # O primeiro a entrar recebe 1
    player = 1
    # Apesar do server escutar até 6 conexões, só suporta 2
    while len(clients) < 2:
        conn, addr = s.accept()
        clients.append(conn)
        print("Cliente conectado de:", addr)
        threading.Thread(target=handle_client, args=(conn, player), daemon=True).start()
        player += 1
    s.close()
    
    # Pensei em implementar a interação para aceitar mais players, mas deixa para o futuro
    while True:
        pass

# Já executa a main quando roda o cod
if __name__ == "__main__":
    main()
