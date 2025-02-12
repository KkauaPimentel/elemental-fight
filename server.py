import socket
import pickle
import threading

# Estado global para uma única partida:
# Cada jogador é representado por uma tupla: (objeto, flag)
# Inicialmente, ambos estão como (None, False)
state1 = (None, False)  # Para o jogador 1 (cliente 1)
state2 = (None, False)  # Para o jogador 2 (cliente 2)

lock = threading.Lock()

def handle_client(conn, player):
    global state1, state2
    while True:
        try:
            data_bytes = conn.recv(4096)
            if not data_bytes:
                break
            # Desserializa a mensagem (espera-se uma tupla: (objeto, flag))
            msg = pickle.loads(data_bytes)
            with lock:
                if player == 1:
                    state1 = msg
                else:
                    state2 = msg
                # Envia para cada cliente o estado do oponente
                if player == 1:
                    opponent_state = state2
                else:
                    opponent_state = state1
            conn.sendall(pickle.dumps(opponent_state))
        except Exception as e:
            print(f"Erro no handle_client (player {player}):", e)
            break
    conn.close()
    print(f"Cliente {player} desconectado.")

def udp_discovery():
    """
    Serviço UDP para descoberta automática do servidor.
    Escuta na porta 9000 por mensagens 'DISCOVER_SERVER' e responde com 'SERVER_HERE'.
    """
    UDP_IP = "0.0.0.0"
    UDP_PORT = 9000
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_IP, UDP_PORT))
    print("Serviço UDP de descoberta iniciado na porta", UDP_PORT)
    while True:
        try:
            data, addr = udp_sock.recvfrom(1024)
            if data.decode().strip() == "caca_server":
                udp_sock.sendto("aqui_estou".encode(), addr)
        except Exception as e:
            print("Erro no serviço UDP:", e)

def main():
    # Inicia a thread de descoberta UDP
    threading.Thread(target=udp_discovery, daemon=True).start()
    
    server_ip = "0.0.0.0"
    server_port = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, server_port))
    s.listen(6)
    print(f"Servidor iniciado em {server_ip}:{server_port}")
    
    clients = []
    player = 1
    while len(clients) < 2:
        conn, addr = s.accept()
        clients.append(conn)
        print("Cliente conectado de:", addr)
        threading.Thread(target=handle_client, args=(conn, player), daemon=True).start()
        player += 1
    s.close()
    while True:
        pass

if __name__ == "__main__":
    main()
