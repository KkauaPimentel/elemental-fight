class Jogo:
    def __init__(self, id):
        self.id= id
        self.p0= None
        self.p1= None

        self.p0conn= False
        self.p1conn= False
        self.ready= False
        self.movs= [None, None]

    #atribui ao player seu movimento(direita, esquerda, ataque...) e se já fez ele
    def player_mov(self, player, mov):
        self.movs[player]= mov

        if player==0:
            self.p0conn= True
        else:
            self.p1conn= True
    
    #retorna o movimento dos players(player)    
    def get_p_mov(self, play):
        return self.movs[play]

    #retorna caso haja 2 players conectados
    def conec(self):
        return self.ready
    
    #retorna se ainda há os dois players na partida
    def ambos(self):
        return self.p0conn and self.p1conn
    
    #retorna o vencedor(que tem vida>0, enquando oponente.vida<=0)
    def winner(self):
        if self.p0.get_vida() <= 0 and self.p1.get_vida() > 0:
            return 1
        elif self.p1.get_vida()<= 0 and self.p0.get_vida() > 0:
            return 0
        return -1   
    
    def get_estado(self):
        return {
            'p0_mov': self.movs[0],
            'p1_mov': self.movs[1],
            'p0_vida': self.p0.get_vida() if self.p0 else 0,
            'p1_vida': self.p1.get_vida() if self.p1 else 0,
            'ready': self.ready
        }

    #reseta o game quando uma partida acaba
    def resetar_game(self):
        self.p0conn= False
        self.p1conn= False
        self.p0= None
        self.p1= None
        self.movs= [None, None]
