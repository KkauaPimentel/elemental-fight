class Personagem:

    def __init__(self, nome="player", ataque=15.0, defesa=25.0, vida=250.0):
        self.nome= nome
        self.ataque= ataque
        self.ataqueBase= self.ataque
        self.vida= vida
        self.vidaBase= self.vida
        self.defesa= defesa
        self.defesaBase= self.defesa
        

    def set_atk(self, new):
        self.ataque= max(0, new)

    def set_vida(self, new):
        self.vida= max(0, new)

    def set_nome(self, new):
        self.nome= new

    def set_def(self, new):
        self.defesa= max(0, new)

    def atk(self):
        return self.ataque
    
    def defense(self):
        return self.defesa

    def reset(self):
        self.vida= self.vidaBase
        self.ataque= self.ataqueBase
        self.defesa= self.defesaBase
    
    def __str__(self):
        part1= f"Personagem: {self.nome} | Vida: {self.vida:.2f} |"
        part2= f"Ataque: {self.ataque:.2f} | Defesa: {self.defesa:.2f}"
        return part1 + part2
    