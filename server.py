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
            # Tenta desserializar o dado recebido
            msg = pickle.loads(data_bytes)  # msg é uma tupla: (objeto, flag)
            with lock:
                if player == 1:
                    state1 = msg
                else:
                    state2 = msg
                # Para cada cliente, o estado enviado é o do oponente:
                if player == 1:
                    opponent_state = state2
                else:
                    opponent_state = state1
            # Envia o estado do oponente
            conn.sendall(pickle.dumps(opponent_state))
        except Exception as e:
            print(f"Erro no handle_client (player {player}):", e)
            break
    conn.close()
    print(f"Cliente {player} desconectado.")

def main():
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
    # O servidor não termina aqui (ou pode ficar num loop infinito se desejar)
    while True:
        pass

if __name__ == "__main__":
    main()
