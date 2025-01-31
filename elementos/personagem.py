import pygame as pg

class Personagem:
    def __init__(self, nome="player", ataque=15.0, defesa=25.0, vida=250.0, x= 300, y=250, largura= 25, altura= 25, cor=(255,0,0)):
        self.nome= nome
        self.ataqueBase= ataque
        self.ataque= self.ataqueBase
        self.vidaBase= vida
        self.vida= self.vidaBase
        self.defesaBase= defesa
        self.defesa= self.defesaBase
        self.largura= largura
        self.altura= altura
        self.cor= cor 
        self.retang= pg.Rect(x, y, largura, altura)
        self.vel= 1

    def desenhar(self, tela):
        pg.draw.rect(tela, self.cor, self.retang)

    def mov(self, tela_l, tela_a):
        keys= pg.key.get_pressed()

        if keys[pg.K_LEFT]:#ESQUERDA
            self.retang.x -= self.vel
        if keys[pg.K_RIGHT]:#DIREITA
            self.retang.x += self.vel
        if keys[pg.K_UP]:#CIMA
            self.retang.y -= self.vel
        if keys[pg.K_DOWN]:#BAIXO
            self.retang.y += self.vel
        
        #garante que os personagens irão ficar no limite da tela
        self.retang.x= max(0, min(self.retang.x, tela_l - self.largura))
        self.retang.y= max(0, min(self.retang.y, tela_a - self.altura))
        
        
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

    #reseta os status dos personagens(usado pós buff)
    def reset(self):
        self.vida= self.vidaBase
        self.ataque= self.ataqueBase
        self.defesa= self.defesaBase
    
    def __str__(self):
        part1= f"Personagem: {self.nome} | Vida: {self.vida:.2f} |"
        part2= f"Ataque: {self.ataque:.2f} | Defesa: {self.defesa:.2f}"
        return part1 + part2
