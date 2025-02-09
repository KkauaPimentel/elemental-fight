import socket
import pickle

class Rede:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = '127.0.0.1'
        self.porta = 5555
        self.end = (self.ip, self.porta)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.end)
            print('Cliente conectado ao servidor')
            resp = self.client.recv(4096 * 2).decode()
            if resp:
                return resp
            else:
                print('Erro ao conectar ao servidor')
                return None
        except Exception as e:
            print('Erro de conexão:', e)
            return None

    def enviar(self, dado):
        try:
            self.client.send(pickle.dumps(dado))
            resp = self.client.recv(4096 * 2)
            return pickle.loads(resp) if resp else None
        except Exception as e:
            print("Erro ao enviar dados:", e)
            return None
