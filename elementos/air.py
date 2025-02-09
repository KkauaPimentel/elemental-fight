from .personagem import Personagem

class Ar(Personagem):
    
    def __init__(self, nome="Ar"):
        super().__init__(nome)
        self.tipo= 'ar'
        self.set_atk(self.ataque + 35)
        self.ataqueBase= self.ataque
        self.set_vida(self.vida - 40)
        self.vidaBase= self.vida
        self.set_def(self.defesa - 7)
        self.defesaBase= self.defesa
    
    def habilidade1(self):
        return (self.atk() * 1.4)
    
    def habilidade2(self):
        self.set_vida(self.vida * 1.5)
        self.set_atk(self.ataque * 1.5)
        return "Modo turbo ativado!"
    
    def __str__(self):
        return f"Ar - {super().__str__()}"
    
# player= Ar("air")
# print(player)
# player.turbo()
# print(player)

    