from  .personagem import Personagem

class Agua(Personagem):
    
    def __init__(self, nome="Água"):
        super().__init__(nome)
        
        self.tipo= 'agua'
        self.ataqueBase = self.ataque + 5
        self.vidaBase = self.vida + 10
        self.set_atk(self.ataqueBase)
        self.set_vida(self.vidaBase)

    def habilidade1(self):
        return (self.atk() * 1.15)
    

    def habilidade2(self):
        regeneracao= (self.vidaBase - self.vida) * 0.4
        self.set_vida(self.vida + regeneracao)
        return f"vida +{regeneracao:.2f}!"
    

    def __str__(self):
        return f"Água - {super().__str__()}"
    
# player= Agua("water")
# print(player)
    