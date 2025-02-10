from .personagem import Personagem

class Avatar(Personagem):
    def __init__(self, nome="Avatar"):
        super.__init__(nome)
        self.tipo= 'avatar'
        # self.set_nome(nome)
        self.set_vida(300)
        self.vidaBase= self.vida
        self.set_def(999)
        self.defesaBase= self.defesa
        self.set_atk(99)
        self.ataqueBase= self.ataque
    
    def habilidade1(self):
        return super().habilidade1()

    def habilidade2(self):
        return super().habilidade2()
    
    def caminhos(self):
        pass
