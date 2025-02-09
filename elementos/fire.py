from .personagem import Personagem

class Fogo(Personagem):
    
    def __init__(self, nome="Fogo"):
        super().__init__(nome)
        self.tipo= 'fogo'
        self.set_atk(self.ataque + 20)
        self.ataqueBase= self.ataque
        
    def habilidade1(self):
        return self.atk() * 1.3
    
    def habilidade2(self):
        self.set_atk(self.ataque * 1.2)
        self.set_def(self.defesa * 1.2)
        # return "Ira ativada, buff em defesa e ataque!"  
    
    def __str__(self):
        return f"Fogo - {super().__str__()}"


# player= Fogo("fire")
# print(player)
# player.ira()
# print(player)