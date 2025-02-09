from .personagem import Personagem

class Terra(Personagem):
    
    def __init__(self, nome="Terra"):
        super().__init__(nome)
        
        self.tipo= 'terra'
        self.set_atk(self.ataque + 3)
        self.ataqueBase= self.ataque
        self.set_vida(self.vida + 50)
        self.vidaBase= self.vida
        self.set_def(self.defesa + 21)
        self.defesaBase= self.defesa
    
    def habilidade1(self):
        return self.atk() * 1.3
    
    def habilidade2(self):
        self.set_vida(self.vida * 1.6)
        self.set_def(self.defesa * 1.6)
        return "Armadura pronta!"
    
    def __str__(self):
        return f"Terra - {super().__str__()}"
    
player= Terra("earth")
print(player)
# player.warrior()
# print(player)
    