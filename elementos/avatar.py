from .water import Agua
from .fire import Fogo
from .earth import Terra
from .air import Ar

class Avatar(Agua, Fogo, Terra, Ar):
    def __init__(self, nome="Avatar"):
        self.tipo= 'avatar'
        self.set_nome(nome)
        self.set_vida(300)
        self.vidaBase= self.vida
        self.set_def(999)
        self.defesaBase= self.defesa
        self.set_atk(99)
        self.ataqueBase= self.ataque
    
    def caminhos(self):
        pass

# player= Avatar("aang")
# print(player)
# player.ira()
# print(player)
# player.warrior()
# print(player)
# player.turbo()
# print(player)
# player.caminhos()
# print(player)

