from .personagem import Personagem

class Madeira(Personagem):
    
    def __init__(self, nome='Madeira'):
        super().__init__(nome)
        
        self.tipo= 'madeira'
        self.set_atk(self.ataque - 8)
        self.ataqueBase= self.ataque
        self.set_vida(self.vida + 70)
        self.vidaBase= self.vida
        self.set_def(self.defesa + 21)
        self.defesaBase= self.defesa
    
    def habilidade1(self):
        return (self.atk() * 1.2)
    
    def habilidade2(self):
        return self.set_atk((self.ataque * 1.2) + 10)
    
    def __str__(self):
        return f"Madeira - {super().__str__()}"

# player= Madeira("wood")
# print(player)
# player.capinar()
# print(player)